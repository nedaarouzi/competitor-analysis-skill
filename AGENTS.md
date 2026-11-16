# Agent instructions

This repository contains open skills for marketing competitor analysis.

- **Competitor dashboard** (preferred when the user asks for a dashboard, tracker, ad intelligence or a spreadsheet of competitor ads): `skills/competitor-dashboard/SKILL.md`. Read it and follow it. You do the research and write the JSON input; `skills/competitor-dashboard/scripts/build_dashboard.py` builds the workbook. Never hand-build the workbook with your own styling.
- **Competitor analysis** (lighter, five-tab version): `skills/competitor-analysis/SKILL.md`.
- Required inputs: a company name and three competitors. Do not ask for anything else unless it is missing and essential. If no competitors are given, choose the 3 to 4 most direct and say why.
- Use public data only. Never invent figures. Mark anything you could not find as "not available".
- Present estimates as ranges with a confidence level, and say clearly that they show direction, not truth.

When editing this repository: keep each `SKILL.md` under 500 lines, keep each `name` field identical to its folder name, change dashboard styling only in `build_dashboard.py`, and do not add company-confidential data.
