# Style guide

The style lives in code, in `scripts/build_dashboard.py` (the `C` colour dictionary, the `WIDTHS` table and the helper functions). Change it there, never in the agent's own output. This page describes the rules so you know what to expect.

## Every tab

- Gridlines off. Dark background (`0A0A0F`) on all cells.
- Row 1 title bar, row 2 subtitle bar (gold text on slate), row 3 spacer, row 4 column headers, data from row 5.
- Panes frozen at `A4`. Landscape, fit to one page wide.
- Arial 10. Data rows alternate `0D1117` and `111827`.

## Focal company

- Company name in orange (`F97316`), bold.
- Active channel rows `1A2A0A`, inactive `2D0A0A`.

## Status and number colours

- Active: `A7F3D0`. Not active: `FCA5A5`. No data: `475569`.
- Budgets in teal (`A5F3FC`). Totals in gold (`FCD34D`).
- Opportunity priority cells filled `FCA5A5` (Immediate), `FCD34D` (30-Day), `86EFAC` (60-Day) with dark text.

## Channel section colours (Actuals tab)

| Channel | Background | Text |
|---|---|---|
| Google | `14532D` | `A7F3D0` |
| Meta | `7C2D12` | `FED7AA` |
| Bing | `164E63` | `A5F3FC` |
| TikTok | `7F1D1D` | `FCA5A5` |
| LinkedIn | `1E3A5F` | `F1F5F9` |
| YouTube | `1E1B4B` | `DDD6FE` |
| Reddit | `431407` | `FCD34D` |
| DSP | `334155` | `F1F5F9` |

## Estimated versus verified

- Actuals tab headers start with "⚠️ ESTIMATED —" unless verified numbers were supplied.
- Tabs 3 and 4 end with a footnote: competitor figures are estimates, and (✓) marks verified focal figures.
- Tab 8 says whether it is based on estimated or verified data.
