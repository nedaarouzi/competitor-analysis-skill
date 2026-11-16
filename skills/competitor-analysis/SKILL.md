---
name: competitor-analysis
description: Run a marketing competitor analysis from a company name and 3 to 4 competitors, and deliver an 8-tab dark-themed Excel competitor ad intelligence dashboard. Estimates each competitor's advertising, platforms, budget, CPL, messaging and remarketing from public ad data, finds gaps, and builds the workbook with a fixed script so the result is the same every time. Use for competitor research, competitor dashboards, ad landscapes or go-to-market research.
license: MIT
metadata:
  author: Neda Arouzi
  version: "1.0.0"
---

# Competitor analysis dashboard

Produces the same 8-tab Excel dashboard every time. **You do the research. A script does the layout.** Never hand-build the workbook with your own styling: the script is what makes results identical between agents and runs.

## Inputs

1. **Focal company** (the company the dashboard is for), plus its segment if given.
2. **3 to 4 competitors.** If the person does not give them, research and pick the 3 to 4 most direct competitors, then say who you chose and why.

Do not ask for anything else. Infer the industry, country and channels from the names. Optional: one or two real numbers from the focal company's own data (for example its CPL or monthly spend). If supplied, mark them verified and use them to calibrate the competitor estimates.

## Steps

1. **Research** (public data only). For the focal company and each competitor, collect: positioning and tagline, pricing model, which of the 8 channels they are active on, ad angle, headlines, targeting signals, creative formats, CTAs, and signs of remarketing. Sources: Meta Ad Library, Google Ads Transparency Center, LinkedIn Ad Library, TikTok Creative Center, the companies' own sites and pricing pages, reputable news. If a source cannot be reached, say so and write "not available". Never invent a figure.
2. **Estimate** monthly budget and CPL per company per channel, as ranges in GBP. Use `references/benchmarks.json` as the starting point and `references/estimation.md` for scaling rules. Give a confidence level (low, medium or high) for each company.
3. **Write the input file** (JSON) to match `templates/input.example.json`. Field rules are in `references/input-schema.md`. The focal company's channels need a `note` where a channel is untested.
4. **Find 6 to 9 opportunities** for the focal company, classed Immediate, 30-Day or 60-Day (rules below).
5. **Build the workbook:**
   ```
   pip install openpyxl
   python scripts/build_dashboard.py my_input.json -o acme_competitor_dashboard.xlsx
   ```
   The script validates the input, prints warnings or errors, and writes the file. If it reports an error, fix the JSON and run it again. Do not patch the output by hand.
6. **Deliver** the .xlsx with a one-line summary. Say who the competitors are, that the figures are estimates, and the single biggest opportunity. Do not list the tab names.

If you cannot run Python in your environment, write the JSON file, give it to the person with the command above, and say that the dashboard needs that one step to be built. Do not substitute a differently styled spreadsheet.

## The 8 tabs (fixed order, built by the script)

| # | Tab | Contents |
|---|---|---|
| 1 | Overview | One row per company: pricing, tagline, positioning, strength, weakness, channels active, confidence |
| 2 | {Company} Actuals | Focal company by channel. Labelled "ESTIMATED" unless verified actuals were supplied |
| 3 | Budget Estimates | Monthly spend range per company per channel, with totals |
| 4 | CPL Estimates | Cost per lead per company per channel, colour-coded against the benchmark |
| 5 | Channel Benchmarks | Category budget and CPL ranges for the 8 channels |
| 6 | Competitor Profiles | One row per company per channel: angle, copy, targeting, creative, CTA, insight |
| 7 | Remarketing | One row per company per channel: audiences, tactic, budget, message, window, offer |
| 8 | Opportunities | 6 to 9 prioritised opportunities |

The 8 channels are Google, Meta, LinkedIn, TikTok, Bing, YouTube, Reddit and DSP. Look at all 8 for every company, even if the answer is "not active".

## Opportunity rules

- **Immediate:** this week, little or no creative needed.
- **30-Day:** needs some setup or creative production.
- **60-Day:** new channels, structural changes or longer experiments.

Common types: remarketing or RLSA gaps; winning creative not scaled; channels competitors use that the focal company has not tested; budget concentrated in high-CPL campaigns; mobile versus desktop conversion gaps; geographic over or under-investment; brand assets missing from ad copy; first-mover tests on low-competition channels. Each opportunity needs a specific action and a reason grounded in what you found.

## Honesty rules

- All competitor figures are estimates. Show ranges, not single numbers, and say they show direction, not truth.
- Mark focal-company figures as verified only if the person gave you the number in this conversation.
- Public data only. Do not use confidential company data unless the person supplies it for calibration.
- Before real budget moves, a person with judgement must check the numbers that matter.

## Keeping it current

Markets move quickly. Tell the person to re-run the dashboard regularly. The run date is shown on every tab so runs can be compared.
