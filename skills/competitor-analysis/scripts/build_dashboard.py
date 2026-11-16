#!/usr/bin/env python3
"""Build the 8-tab competitor ad intelligence dashboard from a JSON file.

Usage:
    python build_dashboard.py input.json [-o output.xlsx]

The agent does the research and writes input.json (see ../templates/input.example.json
and ../references/input-schema.md). This script does all of the layout, so the
workbook looks the same whichever agent or person runs it.

Requires: Python 3.8+ and openpyxl (pip install openpyxl).
"""
import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.cell.cell import MergedCell

HERE = Path(__file__).resolve().parent
BENCH_PATH = HERE.parent / "references" / "benchmarks.json"

# ---------------------------------------------------------------- style ----
C = {
    "bg": "0A0A0F", "hdr": "0F172A", "orange": "F97316", "orange_l": "FED7AA",
    "blue_h": "1E3A5F", "green_h": "14532D", "green_l": "A7F3D0", "red_l": "FCA5A5",
    "purple_h": "5B21B6", "purple_l": "DDD6FE", "gold_h": "78350F", "gold_l": "FCD34D",
    "slate": "334155", "slate_l": "94A3B8", "white": "F1F5F9", "teal_l": "A5F3FC",
    "dark1": "0D1117", "dark2": "111827",
    "row_own_active": "1A2A0A", "row_own_inactive": "2D0A0A",
}

CHANNELS = [  # key, label, section header bg, section header text
    ("Google",   "🔍 Google",   "14532D", "A7F3D0"),
    ("Meta",     "📘 Meta",     "7C2D12", "FED7AA"),
    ("Bing",     "🪟 Bing",     "164E63", "A5F3FC"),
    ("TikTok",   "🎵 TikTok",   "7F1D1D", "FCA5A5"),
    ("LinkedIn", "💼 LinkedIn", "1E3A5F", "F1F5F9"),
    ("YouTube",  "▶️ YouTube",  "1E1B4B", "DDD6FE"),
    ("Reddit",   "🔴 Reddit",   "431407", "FCD34D"),
    ("DSP",      "📡 DSP",      "334155", "F1F5F9"),
]
# Column order used in the budget and CPL matrices (Tabs 3 and 4)
MATRIX_ORDER = ["Google", "Meta", "LinkedIn", "TikTok", "Bing", "YouTube", "Reddit", "DSP"]
LABEL = {k: lbl for k, lbl, _, _ in CHANNELS}

PRIORITY = {
    "immediate": ("🔴 Immediate", "FCA5A5", 7, 0),
    "30-day":    ("🟡 30-Day",    "FCD34D", 30, 1),
    "60-day":    ("🟢 60-Day",    "86EFAC", 60, 2),
}

WIDTHS = {
    1: {"A": 5, "B": 20, "C": 22, "D": 22, "E": 48, "F": 45, "G": 45, "H": 28, "I": 14},
    2: {"A": 40, "B": 26, "C": 14, "D": 14, "E": 12, "F": 65},
    3: {"A": 22, "B": 16, "C": 16, "D": 14, "E": 14, "F": 12, "G": 14, "H": 12, "I": 16, "J": 12, "K": 12},
    4: {"A": 22, "B": 20, "C": 20, "D": 18, "E": 18, "F": 18, "G": 18, "H": 18, "I": 18},
    5: {"A": 16, "B": 22, "C": 16, "D": 26, "E": 78},
    6: {"A": 20, "B": 14, "C": 12, "D": 22, "E": 38, "F": 30, "G": 36, "H": 12, "I": 58},
    7: {"A": 20, "B": 14, "C": 10, "D": 28, "E": 18, "F": 14, "G": 38, "H": 26, "I": 36, "J": 60},
    8: {"A": 5, "B": 16, "C": 6, "D": 36, "E": 22, "F": 82, "G": 30},
}


def fill(h):
    return PatternFill("solid", start_color=h, fgColor=h)


def bdr():
    s = Side(style="thin", color="1E293B")
    return Border(left=s, right=s, top=s, bottom=s)


def fnt(bold=False, color="CBD5E1", sz=10, name="Arial"):
    return Font(name=name, bold=bold, color=color, size=sz)


def aln(h="left", v="center", wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)


def title_row(ws, row, text, bg="0F172A", fg="F1F5F9", sz=11, cols=20):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=cols)
    c = ws.cell(row=row, column=1, value=text)
    c.font = Font(name="Arial", bold=True, color=fg, size=sz)
    c.fill = fill(bg)
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 22


def hdr_row(ws, row, cols_list, bg="1E3A5F", fg="F1F5F9", h=20):
    for ci, val in enumerate(cols_list, 1):
        c = ws.cell(row=row, column=ci, value=val)
        c.font = fnt(bold=True, color=fg)
        c.fill = fill(bg)
        c.alignment = aln("center", "center", True)
        c.border = bdr()
    ws.row_dimensions[row].height = h


def data_cell(ws, row, col, val, bg=None, bold=False, color="CBD5E1", wrap=False, halign="left"):
    c = ws.cell(row=row, column=col, value=val)
    c.font = fnt(bold=bold, color=color)
    if bg:
        c.fill = fill(bg)
    c.alignment = aln(halign, "center", wrap)
    c.border = bdr()
    return c


def set_widths(ws, w_dict):
    for col, w in w_dict.items():
        ws.column_dimensions[col].width = w


# -------------------------------------------------------------- helpers ----
def slugify(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "company"


def safe_sheet_name(name):
    return re.sub(r"[\[\]:*?/\\]", "", name)[:31]


def money(v):
    """£400, £1.5k, £12k. Fixes the integer-division rounding of simple //1000 formatting."""
    if v < 1000:
        return f"£{v:,.0f}"
    k = v / 1000
    return f"£{k:.0f}k" if abs(k - round(k)) < 1e-9 else f"£{k:.1f}k"


def budget_text(rng):
    if not rng:
        return "—"
    lo, hi = rng
    if lo == 0 and hi == 0:
        return "—"
    return money(lo) if lo == hi else f"{money(lo)} – {money(hi)}"


def small_money(v):
    s = f"£{v:,.2f}"
    return s[:-3] if s.endswith(".00") else s


def cpl_text(v):
    if v is None:
        return "—"
    if isinstance(v, (list, tuple)):
        lo, hi = v
        return small_money(lo) if lo == hi else f"{small_money(lo)} – {small_money(hi)}"
    return small_money(v)


def cpl_mid(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        return (v[0] + v[1]) / 2
    return float(v)


def est_height(ws_widths, row_vals, minimum=36, maximum=90):
    """Estimate a row height for wrapped text from the longest cell relative to its column width."""
    lines = 1
    for col_letter, text in row_vals:
        if not text:
            continue
        w = ws_widths.get(col_letter, 12)
        per_line = max(int(w * 1.05), 1)
        n = sum(max(1, math.ceil(len(part) / per_line)) for part in str(text).split("\n"))
        lines = max(lines, n)
    return max(minimum, min(maximum, lines * 13 + 6))


def col_letter(i):
    from openpyxl.utils import get_column_letter
    return get_column_letter(i)


def is_active(company, ch):
    return bool(company.get("channels", {}).get(ch, {}).get("active"))


def active_labels(company):
    return ", ".join(LABEL[k] for k, *_ in CHANNELS if is_active(company, k)) or "—"


def sheet_base(ws, title, subtitle, widths):
    ws.sheet_view.showGridLines = False
    set_widths(ws, widths)
    title_row(ws, 1, title, bg=C["hdr"], fg=C["white"], sz=12)
    title_row(ws, 2, subtitle, bg=C["slate"], fg=C["gold_l"], sz=9)
    ws.row_dimensions[2].height = 18
    ws.row_dimensions[3].height = 8
    ws.freeze_panes = "A4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws._ncols = len(widths)


def paint_background(ws, last_row, cols=20):
    ws.print_area = f"A1:{col_letter(getattr(ws, '_ncols', 10))}{last_row}"
    for r in range(1, last_row + 4):
        for c in range(1, cols + 1):
            cell = ws.cell(row=r, column=c)
            if isinstance(cell, MergedCell):
                continue
            if cell.fill is None or cell.fill.fill_type is None:
                cell.fill = fill(C["bg"])


def row_bg(i):
    return C["dark1"] if i % 2 == 0 else C["dark2"]


# ----------------------------------------------------------- validation ----
def validate(data):
    errors, warnings = [], []
    if "focal" not in data or not data["focal"].get("name"):
        errors.append("'focal' with a 'name' is required.")
    comps = data.get("competitors", [])
    if not comps:
        errors.append("'competitors' must list at least one company.")
    if len(comps) < 3 or len(comps) > 4:
        warnings.append(f"{len(comps)} competitors given; the skill expects 3 to 4.")
    names = [data.get("focal", {}).get("name")] + [c.get("name") for c in comps]
    if len(set(names)) != len(names):
        errors.append("Company names must be unique.")
    for co in [data.get("focal", {})] + comps:
        for ch in co.get("channels", {}):
            if ch not in LABEL:
                errors.append(f"{co.get('name')}: unknown channel '{ch}'. Use one of: {', '.join(LABEL)}.")
    opps = data.get("opportunities", [])
    if not 6 <= len(opps) <= 9:
        warnings.append(f"{len(opps)} opportunities given; the skill expects 6 to 9.")
    for o in opps:
        if str(o.get("priority", "")).lower() not in PRIORITY:
            errors.append(f"Opportunity '{o.get('title')}': priority must be Immediate, 30-Day or 60-Day.")
    return errors, warnings


# ----------------------------------------------------------------- tabs ----
def tab_overview(wb, data, meta):
    ws = wb.active
    ws.title = "Overview"
    sub = meta["subtitle"]
    sheet_base(ws, f"{meta['focal']} — Competitor Ad Intelligence Overview", sub, WIDTHS[1])
    hdr_row(ws, 4, ["#", "Company", "Pricing model", "Tagline", "Positioning", "Key strength",
                    "Key weakness", "Channels active", "Confidence"], bg=C["blue_h"], h=28)
    companies = [data["focal"]] + data["competitors"]
    r = 5
    for i, co in enumerate(companies):
        own = i == 0
        bg = C["row_own_active"] if own else row_bg(i)
        data_cell(ws, r, 1, i + 1, bg, halign="center")
        data_cell(ws, r, 2, co["name"] + (" (focal)" if own else ""), bg, bold=True,
                  color=C["orange"] if own else C["white"], wrap=True)
        data_cell(ws, r, 3, co.get("pricing", "not available"), bg, wrap=True)
        data_cell(ws, r, 4, co.get("tagline", "not available"), bg, wrap=True)
        data_cell(ws, r, 5, co.get("positioning", "not available"), bg, wrap=True)
        data_cell(ws, r, 6, co.get("strength", "not available"), bg, wrap=True, color=C["green_l"])
        data_cell(ws, r, 7, co.get("weakness", "not available"), bg, wrap=True, color=C["red_l"])
        data_cell(ws, r, 8, active_labels(co), bg, wrap=True)
        data_cell(ws, r, 9, co.get("confidence", "low"), bg, halign="center")
        ws.row_dimensions[r].height = est_height(
            WIDTHS[1], [(col_letter(c), ws.cell(row=r, column=c).value) for c in range(2, 9)], 52, 110)
        r += 1
    paint_background(ws, r)


def tab_actuals(wb, data, meta, bench):
    focal = data["focal"]
    ws = wb.create_sheet(safe_sheet_name(f"{focal['name']} Actuals"))
    verified_any = any(focal.get("channels", {}).get(k, {}).get("verified") for k in LABEL) or bool(focal.get("actuals"))
    sub = ("Verified actuals supplied by the user where marked ✓. All other figures are estimated benchmarks."
           if verified_any else
           "⚠️ ESTIMATED — no verified actuals were supplied. Figures are benchmarks adjusted for the company's size and maturity.")
    sheet_base(ws, f"{focal['name']} — Own Performance by Channel", sub, WIDTHS[2])
    r = 4
    for key, label, hbg, hfg in CHANNELS:
        ch = focal.get("channels", {}).get(key, {})
        actuals = (focal.get("actuals") or {}).get(key)
        is_verified = bool(actuals) or bool(ch.get("verified"))
        status = "✅ Active" if ch.get("active") else "❌ Not Active"
        prefix = "" if is_verified else "⚠️ ESTIMATED — "
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        c = ws.cell(row=r, column=1, value=f"{prefix}{label}   |   {status}")
        c.font = Font(name="Arial", bold=True, color=hfg, size=10)
        c.fill = fill(hbg)
        c.alignment = aln("left", "center")
        ws.row_dimensions[r].height = 18
        r += 1
        hdr_row(ws, r, ["Metric", "Value", "Basis", "Benchmark", "vs bench", "Notes"], bg=C["slate"])
        r += 1
        rows = []
        if actuals:
            for m in actuals.get("metrics", []):
                rows.append((m.get("metric"), m.get("value"), m.get("basis", "✓ Verified"),
                             m.get("benchmark", ""), m.get("vs", ""), m.get("note", "")))
        else:
            b = bench[key]
            rows.append(("Status", status, "Est.", "", "", ch.get("note", "Not yet tested." if not ch.get("active") else "")))
            if ch.get("active"):
                rows.append(("Monthly budget", budget_text(ch.get("budget")), "✓ Verified" if ch.get("verified") else "Est.",
                             budget_text(b["budget"]), "", ""))
                mid = cpl_mid(ch.get("cpl"))
                lo, hi = b["cpl"]
                vs = ""
                if mid is not None:
                    bm = (lo + hi) / 2
                    vs = "Below" if mid <= lo else ("Above 2×" if mid >= 2 * bm else ("Above" if mid > hi else "In range"))
                rows.append(("Cost per lead", cpl_text(ch.get("cpl")), "✓ Verified" if ch.get("verified") else "Est.",
                             f"{small_money(lo)} – {small_money(hi)}", vs, ""))
            else:
                rows.append(("Monthly budget", "—", "", budget_text(b["budget"]), "", "Channel not yet tested."))
        for j, (m, v, basis, bm, vs, note) in enumerate(rows):
            bg = (C["row_own_active"] if ch.get("active") else C["row_own_inactive"])
            data_cell(ws, r, 1, m, bg, bold=True, color=C["white"])
            vcol = C["green_l"] if (m == "Status" and ch.get("active")) else (C["red_l"] if m == "Status" else C["white"])
            data_cell(ws, r, 2, v, bg, color=vcol, halign="center")
            data_cell(ws, r, 3, basis, bg, halign="center")
            data_cell(ws, r, 4, bm, bg, halign="center")
            ccol = {"Below": C["green_l"], "In range": C["gold_l"], "Above": C["gold_l"], "Above 2×": C["red_l"]}.get(vs, "CBD5E1")
            data_cell(ws, r, 5, vs, bg, color=ccol, halign="center")
            data_cell(ws, r, 6, note, bg, wrap=True)
            ws.row_dimensions[r].height = 18 if not note or len(str(note)) < 70 else 36
            r += 1
        r += 1
    paint_background(ws, r)


def _matrix(wb, data, meta, bench, name, title, kind):
    ws = wb.create_sheet(name)
    tabno = 3 if kind == "budget" else 4
    sheet_base(ws, title, meta["subtitle"], WIDTHS[tabno])
    heads = ["Company"] + [LABEL[k] for k in MATRIX_ORDER]
    if kind == "budget":
        heads += ["Total (low)", "Total (high)"]
    hdr_row(ws, 4, heads, bg=C["green_h"] if kind == "budget" else C["purple_h"], h=28)
    companies = [data["focal"]] + data["competitors"]
    r = 5
    for i, co in enumerate(companies):
        own = i == 0
        base = row_bg(i)
        data_cell(ws, r, 1, co["name"], C["row_own_active"] if own else base, bold=True,
                  color=C["orange"] if own else C["white"])
        tot_lo = tot_hi = 0
        for ci, key in enumerate(MATRIX_ORDER, 2):
            chd = co.get("channels", {}).get(key, {})
            active = bool(chd.get("active"))
            bg = (C["row_own_active"] if active else C["row_own_inactive"]) if own else base
            mark = " (✓)" if own and chd.get("verified") else ""
            if kind == "budget":
                rng = chd.get("budget") if active else None
                txt = budget_text(rng)
                if rng:
                    tot_lo += rng[0]
                    tot_hi += rng[1]
                color = C["teal_l"] if txt != "—" else "475569"
                data_cell(ws, r, ci, txt + (mark if txt != "—" else ""), bg, color=color, halign="center")
            else:
                v = chd.get("cpl") if active else None
                txt = cpl_text(v)
                if txt == "—":
                    color = "475569"
                elif not own:
                    color = C["green_l"]
                else:
                    lo, hi = bench[key]["cpl"]
                    mid, bm = cpl_mid(v), (lo + hi) / 2
                    color = C["green_l"] if mid <= lo else (C["red_l"] if mid >= 2 * bm else C["gold_l"])
                data_cell(ws, r, ci, txt + (mark if txt != "—" else ""), bg, color=color, halign="center")
        if kind == "budget":
            for off, val in ((10, tot_lo), (11, tot_hi)):
                c = data_cell(ws, r, off, val, base, bold=True, color=C["gold_l"], halign="center")
                c.number_format = '"£"#,##0'
        ws.row_dimensions[r].height = 18
        r += 1
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    c = ws.cell(row=r, column=1, value="* Competitor figures are estimated benchmarks. Focal company figures marked (✓) are verified actuals.")
    c.font = fnt(color=C["slate_l"], sz=9)
    paint_background(ws, r)


def tab_benchmarks(wb, data, meta, bench):
    ws = wb.create_sheet("Channel Benchmarks")
    sheet_base(ws, "Category Benchmarks by Channel",
               "Category-wide starting points in GBP per month. Used to scale the competitor estimates.", WIDTHS[5])
    hdr_row(ws, 4, ["Channel", "Monthly budget range", "CPL range", "Best for", "Notes"], bg=C["gold_h"], h=28)
    r = 5
    for i, key in enumerate(MATRIX_ORDER):
        b = bench[key]
        bg = row_bg(i)
        data_cell(ws, r, 1, LABEL[key], bg, bold=True, color=C["white"])
        data_cell(ws, r, 2, f"{money(b['budget'][0])} – {money(b['budget'][1])}", bg, halign="center", color=C["teal_l"])
        data_cell(ws, r, 3, f"{small_money(b['cpl'][0])} – {small_money(b['cpl'][1])}", bg, halign="center", color=C["gold_l"])
        data_cell(ws, r, 4, b.get("best_for", ""), bg, wrap=True)
        data_cell(ws, r, 5, b.get("note", ""), bg, wrap=True)
        ws.row_dimensions[r].height = est_height(WIDTHS[5], [("D", b.get("best_for")), ("E", b.get("note"))], 36, 70)
        r += 1
    paint_background(ws, r)


def _per_channel_rows(ws, data, meta, kind):
    companies = [data["focal"]] + data["competitors"]
    r = 5
    tabno = 6 if kind == "profile" else 7
    widths = WIDTHS[tabno]
    n = 0
    for i, co in enumerate(companies):
        own = i == 0
        for key, label, *_ in CHANNELS:
            chd = co.get("channels", {}).get(key, {})
            active = bool(chd.get("active"))
            bg = (C["row_own_active"] if active else C["row_own_inactive"]) if own else row_bg(n)
            n += 1
            status = "✅ Active" if active else "❌ Not Active"
            scol = C["green_l"] if active else C["red_l"]
            data_cell(ws, r, 1, co["name"], bg, bold=True, color=C["orange"] if own else C["white"])
            data_cell(ws, r, 2, label, bg)
            data_cell(ws, r, 3, status, bg, color=scol, halign="center")
            if kind == "profile":
                p = chd.get("profile", {}) if active else {}
                vals = [p.get("angle", "—"), p.get("copy", "—"), p.get("targeting", "—"),
                        p.get("creative", "—"), p.get("cta", "—"), p.get("insight", "—")]
                for ci, v in enumerate(vals, 4):
                    data_cell(ws, r, ci, v, bg, wrap=True, halign="center" if ci == 8 else "left")
                last = 9
            else:
                rm = chd.get("remarketing", {}) if active else {}
                rm_active = bool(rm.get("active"))
                data_cell(ws, r, 3, ("✅ Active" if rm_active else "❌ Not Active") if active else "—", bg,
                          color=C["green_l"] if rm_active else C["red_l"], halign="center")
                vals = [rm.get("audiences", "—"), rm.get("tactic", "—"),
                        budget_text(rm.get("budget")) if rm.get("budget") else "—",
                        rm.get("message", "—"), rm.get("window", "—"), rm.get("offer", "—"), rm.get("insight", "—")]
                for ci, v in enumerate(vals, 4):
                    data_cell(ws, r, ci, v, bg, wrap=True, halign="center" if ci == 6 else "left")
                last = 10
            ws.row_dimensions[r].height = 18 if not active else est_height(
                widths, [(col_letter(c), ws.cell(row=r, column=c).value) for c in range(4, last + 1)], 36, 100)
            r += 1
    return r


def tab_profiles(wb, data, meta):
    ws = wb.create_sheet("Competitor Profiles")
    sheet_base(ws, "Competitor Ad Profiles — one row per competitor × channel", meta["subtitle"], WIDTHS[6])
    hdr_row(ws, 4, ["Company", "Channel", "Status", "Angle / hook", "Ad copy and headlines", "Targeting signals",
                    "Creative approach", "CTA", "Insight"], bg=C["blue_h"], h=28)
    r = _per_channel_rows(ws, data, meta, "profile")
    paint_background(ws, r)


def tab_remarketing(wb, data, meta):
    ws = wb.create_sheet("Remarketing")
    sheet_base(ws, "Remarketing Activity — one row per competitor × channel", meta["subtitle"], WIDTHS[7])
    hdr_row(ws, 4, ["Company", "Channel", "Active", "Audiences", "Tactic", "Est. budget", "Message",
                    "Window / frequency", "Offer / CTA", "Insight"], bg=C["purple_h"], h=28)
    r = _per_channel_rows(ws, data, meta, "remarketing")
    paint_background(ws, r)


def tab_opportunities(wb, data, meta):
    ws = wb.create_sheet("Opportunities")
    note = ("Based on verified actuals where marked ✓, otherwise on estimated data. "
            if meta["verified"] else "Based on ESTIMATED data. Validate against real account data before moving budget. ")
    sheet_base(ws, f"Strategic Opportunities for {meta['focal']}", note + "Sorted by urgency.", WIDTHS[8])
    hdr_row(ws, 4, ["#", "Priority", "Days", "Opportunity", "Channel / area", "What to do and why", "Expected impact"],
            bg=C["slate"], h=28)
    opps = sorted(data["opportunities"], key=lambda o: PRIORITY[str(o["priority"]).lower()][3])
    r = 5
    for i, o in enumerate(opps, 1):
        label, colr, days, _ = PRIORITY[str(o["priority"]).lower()]
        bg = row_bg(i)
        data_cell(ws, r, 1, i, bg, halign="center")
        c = data_cell(ws, r, 2, label, colr, bold=True, color=C["bg"], halign="center")
        data_cell(ws, r, 3, days, bg, halign="center", color=colr)
        data_cell(ws, r, 4, o.get("title", ""), bg, bold=True, color=C["white"], wrap=True)
        data_cell(ws, r, 5, o.get("area", ""), bg, wrap=True)
        data_cell(ws, r, 6, o.get("action", ""), bg, wrap=True)
        data_cell(ws, r, 7, o.get("impact", ""), bg, wrap=True)
        ws.row_dimensions[r].height = est_height(
            WIDTHS[8], [("D", o.get("title")), ("E", o.get("area")), ("F", o.get("action")), ("G", o.get("impact"))], 36, 100)
        r += 1
    paint_background(ws, r)


# ----------------------------------------------------------------- main ----
def build(data, out_path):
    bench = json.loads(BENCH_PATH.read_text(encoding="utf-8"))
    for k, v in (data.get("benchmarks") or {}).items():
        bench.setdefault(k, {}).update(v)
    focal = data["focal"]
    verified = any(focal.get("channels", {}).get(k, {}).get("verified") for k in LABEL) or bool(focal.get("actuals"))
    run_date = data.get("run_date") or date.today().isoformat()
    meta = {
        "focal": focal["name"],
        "verified": verified,
        "subtitle": (f"Run date {run_date}. Public-data estimates in GBP. They show direction, not truth. "
                     "Check the numbers that matter before moving real budget."),
    }
    wb = Workbook()
    tab_overview(wb, data, meta)
    tab_actuals(wb, data, meta, bench)
    _matrix(wb, data, meta, bench, "Budget Estimates", "Monthly Ad Spend Estimates (GBP) by Competitor × Channel", "budget")
    _matrix(wb, data, meta, bench, "CPL Estimates", "Cost per Lead Estimates (GBP) by Competitor × Channel", "cpl")
    tab_benchmarks(wb, data, meta, bench)
    tab_profiles(wb, data, meta)
    tab_remarketing(wb, data, meta)
    tab_opportunities(wb, data, meta)
    assert len(wb.sheetnames) == 8
    wb.save(out_path)
    return wb.sheetnames


def main():
    ap = argparse.ArgumentParser(description="Build the 8-tab competitor ad intelligence dashboard.")
    ap.add_argument("input", help="Path to the input JSON file")
    ap.add_argument("-o", "--output", help="Output .xlsx path (default: <company>_competitor_dashboard.xlsx)")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    errors, warnings = validate(data)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    out = args.output or f"{slugify(data['focal']['name'])}_competitor_dashboard.xlsx"
    sheets = build(data, out)
    print(f"Wrote {out} with tabs: {', '.join(sheets)}")


if __name__ == "__main__":
    main()
