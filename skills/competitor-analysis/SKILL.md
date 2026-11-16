---
name: competitor-analysis
description: Run a marketing competitor analysis from just a company name and three competitors. Estimates each competitor's advertising, platforms, approximate budget, cost per acquisition, messaging and retargeting from public ad-library data, finds gaps in the market, and delivers a structured spreadsheet. Use when asked for competitor research, an ad landscape, or go-to-market research.
license: MIT
metadata:
  author: Neda Arouzi
  version: "0.1.0"
---

# Competitor analysis

Produce a structured, shareable competitor analysis for a marketer who needs direction fast.

## Inputs

Ask for these two things only, and only if they are missing:

1. **Company name** (the focal company or product).
2. **Three competitors.**

Do not ask for a long brief. Everything else is optional: market or country, the channel the person cares most about (for example paid social, search, CRM, content), and one real number from their own data (see "Calibrate").

## Sources

Use public data only. Never use confidential or internal company data unless the person supplies it for calibration in this conversation.

- Public ad libraries: Meta Ad Library, Google Ads Transparency Center, LinkedIn Ad Library, TikTok Creative Center.
- The competitors' own websites, landing pages and pricing pages.
- Public company information and reputable news.

If you cannot reach a source, say so and mark the affected cells "not available". Never invent a figure to fill a gap.

## Steps

1. **Collect.** For each competitor, find their active ads and which platforms they run on.
2. **Analyse the ads.** Record the headlines, primary text, angle (for example price, speed, proof, fear of missing out) and creative formats. Note whether there are signs of retargeting (for example the same offer shown at different funnel stages, or urgency and "come back" messaging).
3. **Estimate.** For each competitor, give an approximate monthly budget and an approximate cost per acquisition (CPA). Show a range, not a single figure. State the reasoning in one line: for example the number of active ads, how long they have run, and typical costs for that channel.
4. **Calibrate** (see below).
5. **Find the gaps.** Compare all four companies. List angles, audiences, platforms or offers that nobody uses well, and rank the three best opportunities.
6. **Deliver** the spreadsheet (see "Output").

## Calibrate

Estimates built only from public data tend to be too high or too low. If the person gives one real number from their own data (for example their own CPA, monthly spend or conversion rate), use it as a reference point: compare each competitor with it and adjust the estimates. Say which number you used and how much the estimates moved.

If no number was given, finish the analysis, label every estimate "uncalibrated", and ask once for a single real number.

## Output

Create a spreadsheet with these tabs:

| Tab | Contents |
|---|---|
| Summary | Three to five headlines, the top three opportunities, and the caveats |
| Competitors | One row per competitor: platforms, active ad count, approximate monthly budget (range), approximate CPA (range), retargeting (yes, no or unclear), confidence (low, medium, high) |
| Messaging | One row per ad: competitor, platform, headline, primary text, angle, format, first seen, source link |
| Gaps | Ranked opportunities with the evidence for each |
| Sources | Every link used, with the date it was checked |

Use a Google Sheet if a Google Sheets tool is available. Otherwise create an .xlsx file, or CSV files if that is not possible. Keep the same tabs and column names every time, so results are comparable between runs.

## Honesty rules

- Say clearly that the figures are estimates. They show direction, not truth. They are useful for generating ideas and for understanding the messaging competitors use.
- Give a confidence level for each estimate. Do not present a range as a measurement.
- Before real budget moves, a person with judgement must check the numbers that matter.

## Optional extension

If the person asks, add a "Long-running ads" tab: the angles, headlines and primary text that a competitor has run for more than 45 days. An ad that survives that long is probably working, so it is a useful signal of what works.

## Keeping it current

Markets move quickly, especially in technology and AI. Tell the person to re-run the analysis regularly, and keep each run's date in the Summary tab so they can compare runs.
