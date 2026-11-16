# Agent instructions

This repository contains one open skill for marketing competitor analysis.

- The skill lives in `skills/competitor-analysis/SKILL.md`. Read it and follow it when the user asks for competitor research, a competitor dashboard, an ad landscape or go-to-market research. You do the research and write the JSON input; `skills/competitor-analysis/scripts/build_dashboard.py` builds the Excel dashboard. Never hand-build the workbook with your own styling.
- Required inputs: a company name and three competitors. Do not ask for anything else unless it is missing and essential. If no competitors are given, choose the 3 to 4 most direct and say why.
- Use public data only. Never invent figures. Mark anything you could not find as "not available".
- Present estimates as ranges with a confidence level, and say clearly that they show direction, not truth.

When editing this repository: keep `SKILL.md` under 500 lines, keep the `name` field identical to the folder name, change dashboard styling only in `build_dashboard.py`, and do not add company-confidential data.
