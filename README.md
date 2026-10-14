# LKML
Analyze Linux Kernel Mailing List traffic from [lore.kernel.org](https://lore.kernel.org/lkml/).

`lkml.py` pulls messages through lore's public Atom search API and reports:
- busiest subsystems (from `subsystem: summary` subjects) and target trees (`net-next`, stable `6.12`, ...)
- most active posters and patch authors
- who is reviewing: `Reviewed-by` / `Acked-by` / `Tested-by` trailers in replies (quoted trailers are ignored)
- patch series at their highest revision (`[PATCH v9 0/7] ...`)
- hottest threads and `[REGRESSION]` reports

```sh
python3 lkml.py report                                 # last day of LKML
python3 lkml.py report --since 3.days.ago --pages 5
python3 lkml.py report --query 's:"mm:"' --top 20      # any lore search syntax
python3 lkml.py report --list netdev --json            # other lists on lore
python3 lkml.py report --file saved.atom               # offline
python3 -m pytest tests
```

Standard library only. Fetches at most `--pages` × 200 messages with a pause between pages to be gentle with kernel.org. LKML moves ~200 messages an hour, so a "1 day" query with the default 3 pages covers the most recent few hours.
