# Calm Year 2027 Lite

**Generate a clean, printable 2027 planner PDF in one command – free, offline, MIT-licensed.**

## What it does

`calm_year_lite.py` builds a 15-page planner for freelancers and anyone who likes paper:

- 2027 at a glance (12 mini calendars)
- 12 monthly calendars (Monday start) with "Dates that matter" and "This month's focus"
- 1 blank weekly page (top 3 priorities, day-by-day with billable hours, one calm win) – print it as often as you like
- 1 invoice log page (22 rows: number, client, sent, due, amount, paid on)

Choose A4 or US Letter. The script only writes one PDF into the output folder and refuses
to overwrite an existing file unless you pass `--force`. No network access, nothing is deleted.

## Quick start

```bash
pip install reportlab
python calm_year_lite.py --out out --paper a4
```

Use `--paper letter` for US Letter. Then open `out/Calm-Year-2027-Lite_A4.pdf` and print it at 100 % ("Actual size").

## Requirements

- Python 3.8 or newer
- [reportlab](https://pypi.org/project/reportlab/) (`pip install reportlab`)

## Licence

MIT – see `LICENSE`.

Created with AI assistance by an automated system.

## Full version

The Lite version is a small generator with one weekly page and one invoice page. The full
**Calm Year 2027** printable planner adds, as ready-to-print PDFs:

- all 52 weekly pages, dated, with links to the previous/next week
- clickable month tabs and a section bar for tablet use
- a second plan page per month (income target vs. received, clients, invoices to send, time off)
- goals and income-and-time plan pages, and 4 quarterly reviews
- client tracker (6 pages), client profiles (4 pages) and a 12-page invoice log
- a 2-page year-end review and 20 notes pages (dot grid and lined)
- A4, US Letter and a 6x9 book-interior PDF

Get it here: https://kontor7-agent.github.io/p/calm-year-planner-2027-printable?s=github
