from pathlib import Path

from lkml import analyze, parse_feed, parse_subject

FIXTURE = Path(__file__).parent / "fixture.atom"


def test_parse_subject():
    s = parse_subject("[PATCH net-next v4 3/8] net: bcmgenet: allow the MTU to be changed")
    assert (s.kind, s.tree, s.version, s.index, s.total, s.subsystem, s.is_reply) == ("PATCH", "net-next", 4, 3, 8, "net", False)
    s = parse_subject("Re: [RFC PATCH v2 0/5] x86/virt/tdx: Convert the reader")
    assert (s.kind, s.version, s.index, s.subsystem, s.is_reply) == ("RFC PATCH", 2, 0, "x86/virt/tdx", True)
    s = parse_subject("[GIT PULL] Networking for v6.19-rc1")
    assert s.kind == "GIT PULL"
    assert parse_subject("Linux 6.18").subsystem == ""
    assert parse_subject("[PATCH] mm/slub: fix typo").version == 1


def test_report_from_fixture():
    msgs = parse_feed(FIXTURE.read_bytes())
    assert len(msgs) == 6
    r = analyze(msgs)
    assert r["replies"] == 2
    assert r["with_diff"] == 2
    # quoted trailers don't count, only the reviewer's own
    assert r["reviews"] == {"Reviewed-by": [("Bob Maintainer", 1)], "Tested-by": [("Carol Tester", 1)]}
    assert [s["title"] for s in r["series"]][0].startswith("[PATCH net-next v4 0/2]")
    assert r["regressions"][0]["author"] == "Dan"
    assert r["hot_threads"][0]["messages"] == 3  # the patch and its two replies
    assert r["hot_threads"][0]["participants"] == 3
    assert dict(r["subsystems"])["net"] == 4
