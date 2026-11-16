# Input file reference

The build script reads one JSON file. See `../templates/input.example.json` for a complete working example (fictional companies).

## Top level

| Key | Required | Notes |
|---|---|---|
| `run_date` | no | `YYYY-MM-DD`. Defaults to today. Shown on every tab. |
| `focal` | yes | The company the dashboard is for. |
| `competitors` | yes | 3 to 4 company objects. |
| `opportunities` | yes | 6 to 9 objects (see below). |
| `benchmarks` | no | Overrides for the defaults in `benchmarks.json`, for example `{"Google": {"cpl": [4, 18]}}`. |

## Company object (`focal` and each competitor)

| Key | Notes |
|---|---|
| `name` | Required. Must be unique. |
| `tagline`, `pricing`, `positioning`, `strength`, `weakness` | Short text. Use `"not available"` if unknown. |
| `confidence` | `low`, `medium` or `high`. Reflects how much public ad data you found. |
| `channels` | Object keyed by channel name: `Google`, `Meta`, `LinkedIn`, `TikTok`, `Bing`, `YouTube`, `Reddit`, `DSP`. A channel you leave out is treated as not active. |

## Channel object

| Key | Notes |
|---|---|
| `active` | `true` or `false`. |
| `budget` | `[low, high]` monthly GBP, for example `[3000, 5000]`. |
| `cpl` | A number, or `[low, high]`, in GBP. |
| `verified` | Focal company only. `true` marks budget and CPL as verified actuals and shows (✓). Use only for numbers the person gave you. |
| `note` | Focal company only. Shown on the Actuals tab, for example "Not yet tested". |
| `profile` | `angle`, `copy`, `targeting`, `creative`, `cta`, `insight`. |
| `remarketing` | `active`, `audiences`, `tactic`, `budget` (`[low, high]`), `message`, `window`, `offer`, `insight`. |

## Focal company only: `actuals` (optional)

If the person supplied real performance data, add it per channel and the Actuals tab will use it in place of the estimates:

```json
"actuals": {
  "Google": {"metrics": [
    {"metric": "Cost per lead", "value": "£8.20", "basis": "✓ Verified", "benchmark": "£3 – £15", "vs": "In range", "note": "Last 90 days"}
  ]}
}
```

## Opportunity object

`priority` (`Immediate`, `30-Day` or `60-Day`), `title`, `area` (channel or topic), `action` (what to do and why), `impact`.

## Validation

The script stops with an error for: missing focal company, no competitors, duplicate names, unknown channel names, or an invalid priority. It prints a warning, and still builds, if there are not 3 to 4 competitors or not 6 to 9 opportunities.
