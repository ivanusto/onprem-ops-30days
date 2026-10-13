#!/usr/bin/env python3
"""由 lab/cost.yaml 算一年成本：電費（累進費率的邊際那一段）、硬體攤提、雲端對照。

    python3 scripts/cost.py                 # 印 Markdown 表
    python3 scripts/cost.py --check         # 只驗 cost.yaml 的欄位（CI）
    python3 scripts/cost.py --json          # 機器可讀

沒填的數字印【待填】，含它的總計標「不含待填」。電費依 tariff.kind：
  tiered  場域用電疊在 household_base_kwh_per_month 之上，算多出來的那一段，
          夏季月份用 summer 費率，其餘用 non_summer
  flat    每度一個價
冷氣（有 cop、watts_avg 留 null 的設備）的瓦數由其他設備的平均熱負載除以 cop 推得。
回本只算雲端真的取代的設備：cloud.items[].replaces 列設備 name，分子是那些設備的購入價，
分母是雲端月費減去拿掉那些設備後省下的月電費（累進制下要整體重算，不能按比例分）。
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DAYS_PER_MONTH = 365 / 12
MISSING = "【待填】"
WATTS_SOURCE = {"measured": "實測", "spec": "規格值", "estimate": "估計", "derived": "推得"}


def tier_cost(kwh, tiers, season):
    """累進：從 0 到 kwh 的總電費。"""
    cost, lower = 0.0, 0.0
    for t in tiers:
        upper = t["upto"] if t["upto"] is not None else float("inf")
        if kwh <= lower:
            break
        cost += (min(kwh, upper) - lower) * t[season]
        lower = upper
    return cost


def elec_year(lab_kwh_month, base, tariff):
    """場域每月 lab_kwh_month 度、疊在 base 度上，一年多付的電費。base 為 None 且是累進制時回 None。"""
    if tariff["kind"] == "flat":
        return lab_kwh_month * 12 * tariff["flat_twd_per_kwh"]
    if base is None:
        return None
    summer = len(tariff.get("summer_months") or [])
    tiers = tariff["tiers"]
    total = 0.0
    for season, months in (("summer", summer), ("non_summer", 12 - summer)):
        total += (tier_cost(base + lab_kwh_month, tiers, season) - tier_cost(base, tiers, season)) * months
    return total


def fmt(v, unit=""):
    if v is None:
        return MISSING
    if isinstance(v, float):
        return f"{v:,.0f}{unit}" if abs(v) >= 100 else f"{v:,.1f}{unit}"
    return f"{v:,}{unit}"


def fmt1(v):
    """瓦數與度數一律一位小數。"""
    return MISSING if v is None else f"{v:,.1f}"


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate(c):
    errs = []
    t = c.get("tariff") or {}
    if t.get("kind") not in ("tiered", "flat"):
        errs.append("tariff.kind 要是 tiered 或 flat")
    if t.get("kind") == "tiered":
        tiers = t.get("tiers") or []
        if not tiers or tiers[-1].get("upto") is not None:
            errs.append("tariff.tiers 最後一級的 upto 要是 null")
        last = 0
        for i, x in enumerate(tiers):
            for k in ("non_summer", "summer"):
                if not num(x.get(k)):
                    errs.append(f"tariff.tiers[{i}].{k} 要是數字")
            if x.get("upto") is not None and x["upto"] <= last:
                errs.append(f"tariff.tiers[{i}].upto 要遞增")
            last = x.get("upto") or last
        if not all(1 <= m <= 12 for m in t.get("summer_months") or []):
            errs.append("tariff.summer_months 要是 1 到 12")
    if t.get("kind") == "flat" and not num(t.get("flat_twd_per_kwh")):
        errs.append("tariff.kind 是 flat 時 flat_twd_per_kwh 要是數字")
    for v in t.get("household_base_scenarios") or []:
        if not num(v) or v < 0:
            errs.append("tariff.household_base_scenarios 要是非負數字")
    names = set()
    coolers = 0
    for i, d in enumerate(c.get("devices") or []):
        for k in ("name", "role", "count", "hours_per_day", "amortize_years"):
            if d.get(k) in (None, ""):
                errs.append(f"devices[{i}] 缺 {k}")
        if d.get("name") in names:
            errs.append(f"devices[{i}].name 重複：{d.get('name')}")
        names.add(d.get("name"))
        if d.get("watts_label") is not None and not isinstance(d["watts_label"], str):
            errs.append(f"devices[{i}].watts_label 要是文字")
        for k in ("watts_avg", "price_twd", "residual_twd", "yearly_fee_twd", "count", "hours_per_day", "amortize_years", "cop"):
            if d.get(k) is not None and not num(d[k]):
                errs.append(f"devices[{i}].{k} 要是數字或 null")
        if num(d.get("hours_per_day")) and not 0 < d["hours_per_day"] <= 24:
            errs.append(f"devices[{i}].hours_per_day 要在 0 到 24")
        if num(d.get("amortize_years")) and d["amortize_years"] <= 0:
            errs.append(f"devices[{i}].amortize_years 要大於 0")
        if d.get("watts_source") is not None and d["watts_source"] not in WATTS_SOURCE:
            errs.append(f"devices[{i}].watts_source 要是 {'、'.join(WATTS_SOURCE)} 之一")
        if d.get("cop") is not None:
            coolers += 1
            if num(d["cop"]) and d["cop"] <= 0:
                errs.append(f"devices[{i}].cop 要大於 0")
    if coolers > 1:
        errs.append("只能有一台設備填 cop")
    cl = c.get("cloud") or {}
    scen = cl.get("scenarios") or []
    for i, x in enumerate(cl.get("items") or []):
        for k in ("name", "replaces", "source"):
            if not x.get(k):
                errs.append(f"cloud.items[{i}] 缺 {k}")
        rep = x.get("replaces") or []
        if not isinstance(rep, list):
            errs.append(f"cloud.items[{i}].replaces 要是設備 name 的清單")
        else:
            for r in rep:
                if r not in names:
                    errs.append(f"cloud.items[{i}].replaces 指到不存在的設備：{r}")
        if not ("monthly_usd" in x or "monthly_twd" in x or ("usd_per_hour" in x and "hours_per_month" in x)):
            errs.append(f"cloud.items[{i}] 要有 monthly_twd、monthly_usd 或 usd_per_hour 加 hours_per_month")
        h = x.get("hours_per_month")
        if isinstance(h, dict):
            if set(h) != set(scen):
                errs.append(f"cloud.items[{i}].hours_per_month 的情境要與 cloud.scenarios 一致")
            for v in h.values():
                if v is not None and not (num(v) and 0 <= v <= 744):
                    errs.append(f"cloud.items[{i}].hours_per_month 要在 0 到 744")
        elif h is not None and not (num(h) and 0 <= h <= 744):
            errs.append(f"cloud.items[{i}].hours_per_month 要在 0 到 744")
    return errs


def device_rows(c):
    rows, missing = [], {"kwh": False, "amort": False}
    # 冷氣要移除的熱：其他設備的全天平均瓦數
    heat_w = sum(d["count"] * d["watts_avg"] * d["hours_per_day"] / 24
                 for d in c.get("devices") or [] if d.get("cop") is None and d.get("watts_avg") is not None)
    it_missing = any(d.get("cop") is None and d.get("watts_avg") is None for d in c.get("devices") or [])
    for d in c.get("devices") or []:
        n, w, h = d["count"], d.get("watts_avg"), d["hours_per_day"]
        src = d.get("watts_source")
        if w is None and d.get("cop") is not None and not it_missing:
            w = heat_w / d["cop"] / n
            src = "derived"
        kwh_m = None if w is None else n * w * h * DAYS_PER_MONTH / 1000
        price, fee = d.get("price_twd"), d.get("yearly_fee_twd")
        amort = None
        if price is not None:
            amort = n * (price - (d.get("residual_twd") or 0)) / d["amortize_years"]
        if fee is not None:
            amort = (amort or 0) + fee
        if kwh_m is None:
            missing["kwh"] = True
        if amort is None:
            missing["amort"] = True
        rows.append({"name": d["name"], "role": d["role"], "count": n, "watts_avg": w,
                     "watts_source": d.get("watts_label") or WATTS_SOURCE.get(src, src or ""), "hours_per_day": h,
                     "kwh_per_month": kwh_m, "price_twd": price, "amortization_per_year": amort,
                     "note": d.get("watts_note", "")})
    return rows, missing


def cloud_monthly(x, fx, scenario):
    m = x.get("monthly_twd")
    if m is not None:
        return m
    usd = x.get("monthly_usd")
    h = x.get("hours_per_month")
    if isinstance(h, dict):
        h = h.get(scenario)
    if usd is None and x.get("usd_per_hour") is not None and h is not None:
        usd = x["usd_per_hour"] * h
    return None if (usd is None or fx is None) else usd * fx


def compare(rows, c, base, scenario):
    """一個家戶基礎度數、一個雲端情境下的對照：雲端一年、被取代設備的地端一年、回本月數。"""
    t = c["tariff"]
    cl = c.get("cloud") or {}
    fx = cl.get("fx_twd_per_usd")
    by_name = {r["name"]: r for r in rows}
    replaced = sorted({n for x in cl.get("items") or [] for n in x.get("replaces") or []},
                      key=lambda n: list(by_name).index(n))
    kwh_all = sum(r["kwh_per_month"] or 0 for r in rows)
    kwh_rep = sum(by_name[n]["kwh_per_month"] or 0 for n in replaced)
    rep_incomplete = any(by_name[n]["kwh_per_month"] is None or by_name[n]["price_twd"] is None for n in replaced)
    e_all, e_rest = elec_year(kwh_all, base, t), elec_year(kwh_all - kwh_rep, base, t)
    # 累進制下省下多少要看整體度數，任何一台沒有度數就算不出來
    saved = None if (e_all is None or any(r["kwh_per_month"] is None for r in rows)) else e_all - e_rest
    hw = sum(by_name[n]["count"] * (by_name[n]["price_twd"] or 0) for n in replaced)
    amort = sum(by_name[n]["amortization_per_year"] or 0 for n in replaced)
    monthly = [cloud_monthly(x, fx, scenario) for x in cl.get("items") or []]
    cloud_year = None if any(m is None for m in monthly) else sum(monthly) * 12
    breakeven, never = None, False
    if cloud_year is not None and saved is not None and not rep_incomplete:
        gain = (cloud_year - saved) / 12
        if gain > 0:
            breakeven = hw / gain
        else:
            never = True
    return {"scenario": scenario, "household_base_kwh_per_month": base, "replaced": replaced,
            "replaced_hardware_twd": hw, "replaced_electricity_per_year": saved,
            "replaced_onprem_per_year": None if (saved is None or rep_incomplete) else saved + amort,
            "cloud_monthly_twd": monthly, "cloud_per_year": cloud_year,
            "breakeven_months": breakeven, "never_pays_back": never, "incomplete": rep_incomplete}


def compute(c):
    t = c["tariff"]
    base = t.get("household_base_kwh_per_month")
    rows, missing = device_rows(c)
    kwh_total = sum(r["kwh_per_month"] or 0 for r in rows)
    e_year = None if missing["kwh"] else elec_year(kwh_total, base, t)
    incomplete = missing["kwh"] or missing["amort"] or e_year is None
    for r in rows:
        r["electricity_per_year"] = None if (e_year is None or not kwh_total or r["kwh_per_month"] is None) \
            else e_year * r["kwh_per_month"] / kwh_total
    amort_total = sum(r["amortization_per_year"] or 0 for r in rows)
    cl = c.get("cloud") or {}
    scenarios = cl.get("scenarios") or [None]
    bases = [base] if (base is not None or t["kind"] == "flat") else []
    if t["kind"] == "tiered":
        bases += [b for b in t.get("household_base_scenarios") or [] if b != base]
    by_base = []
    for b in bases or [None]:
        e = None if missing["kwh"] else elec_year(kwh_total, b, t)
        by_base.append({"household_base_kwh_per_month": b, "electricity_per_year": e,
                        "onprem_per_year": None if (e is None or missing["amort"]) else e + amort_total})
    return {"tariff_kind": t["kind"], "summer_months": len(t.get("summer_months") or []),
            "household_base_kwh_per_month": base, "devices": rows, "kwh_per_month_total": kwh_total,
            "electricity_per_year": e_year, "amortization_per_year": amort_total,
            "onprem_per_year": None if incomplete else e_year + amort_total, "incomplete": incomplete,
            "missing_kwh": missing["kwh"], "missing_amortization": missing["amort"], "by_base": by_base,
            "cloud_items": [{"name": x["name"], "replaces": x["replaces"], "source": x["source"],
                             "checked": x.get("checked"), "assumption": x.get("assumption", "")}
                            for x in cl.get("items") or []],
            # 基礎度數填了就只用它對照，沒填才用情境各算一次
            "comparisons": [compare(rows, c, b, s) for b in (bases[:1] if base is not None else bases or [None])
                            for s in scenarios],
            "labor_note": c.get("labor_note", "")}


def months(cmp):
    if cmp["never_pays_back"]:
        return "不會回本"
    v = cmp["breakeven_months"]
    return MISSING if v is None else (f"{v:,.0f}" if v >= 10 else f"{v:.1f}")


def markdown(r, c):
    cur = c.get("currency", "TWD")
    pk = "（不含待填）" if r["missing_kwh"] else ""
    pa = "（不含待填）" if r["missing_amortization"] else ""
    L = ["## 一年成本", "",
         "| 設備項目 | 數量 | 平均功耗 (W) | 數據來源 | 時/日 | 每月度數 (kWh) | 電費/年 | 攤提/年 |",
         "|---|---:|---:|---|---:|---:|---:|---:|"]
    for d in r["devices"]:
        L.append(f"| {d['name']} | {d['count']} | {fmt1(d['watts_avg'])} | {d['watts_source']} | {d['hours_per_day']} "
                 f"| {fmt1(d['kwh_per_month'])} | {fmt(d['electricity_per_year'])} | {fmt(d['amortization_per_year'])} |")
    L.append(f"| **合計** | | | | | **{fmt1(r['kwh_per_month_total'])}{pk}** | **{fmt(r['electricity_per_year'])}** "
             f"| **{fmt(r['amortization_per_year'])}{pa}** |")
    L.append("")
    if r["tariff_kind"] == "tiered":
        L.append(f"電費是累進費率的邊際段：場域每月 {fmt(r['kwh_per_month_total'])} 度疊在 {fmt(r['household_base_kwh_per_month'])} 度的"
                 f"家戶基礎用電上，夏季 {r['summer_months']} 個月用夏季費率，每台的電費是整體邊際按度數比例分配。")
    else:
        L.append("電費以單一費率計算。")
    L += ["", f"地端一年合計（電費加攤提）：**{fmt(r['onprem_per_year'], ' ' + cur)}**" + ("，不完整，有欄位待填" if r["incomplete"] else "")]
    if r["tariff_kind"] == "tiered" and len(r["by_base"]) > 1:
        L += ["", "| 家戶基礎（度/月） | 場域電費/年 | 地端一年（電加攤提） |", "|---:|---:|---:|"]
        for b in r["by_base"]:
            L.append(f"| {fmt(b['household_base_kwh_per_month'])} | {fmt(b['electricity_per_year'])} | {fmt(b['onprem_per_year'])} |")

    cl = c.get("cloud") or {}
    scen = cl.get("scenarios") or [None]
    L += ["", "## 雲端對照", "", "| 項目 | 取代 | " + " | ".join(f"月費（{s}）" if s else "月費" for s in scen) + " | 查價 | 假設 |",
          "|---|---|" + "---:|" * len(scen) + "---|---|"]
    first = {cmp["scenario"]: cmp for cmp in reversed(r["comparisons"])}
    for i, x in enumerate(r["cloud_items"]):
        fees = " | ".join(fmt(first[s]["cloud_monthly_twd"][i]) for s in scen)
        L.append(f"| {x['name']} | {'、'.join(x['replaces'])} | {fees} | [{x['checked'] or MISSING}]({x['source']}) | {x['assumption']} |")
    L.append("")
    head = r["comparisons"][0]
    L.append(f"雲端取代的設備：{'、'.join(head['replaced'])}，購入價合計 {fmt(head['replaced_hardware_twd'], ' ' + cur)}。"
             "回本月數是這筆購入價除以「雲端月費減去拿掉這些設備省下的月電費」。")
    L += ["", "| 家戶基礎（度/月） | 雲端情境 | 雲端一年 | 被取代設備的地端一年（電加攤提） | 回本月數 |", "|---:|---|---:|---:|---:|"]
    for cmp in r["comparisons"]:
        L.append(f"| {fmt(cmp['household_base_kwh_per_month'])} | {cmp['scenario'] or ''} | {fmt(cmp['cloud_per_year'])} "
                 f"| {fmt(cmp['replaced_onprem_per_year'])} | {months(cmp)} |")
    L += ["", f"人力：{r['labor_note']}"]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", default=str(ROOT / "lab" / "cost.yaml"))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    with open(a.file, encoding="utf-8") as f:
        c = yaml.safe_load(f)
    errs = validate(c)
    if errs:
        for e in errs:
            print(f"cost.yaml：{e}", file=sys.stderr)
        return 1
    r = compute(c)
    if a.check:
        done = not r["incomplete"] and all(cmp["cloud_per_year"] is not None for cmp in r["comparisons"])
        print(f"cost.yaml 通過，{len(r['devices'])} 項設備、{len(r['cloud_items'])} 項雲端對照"
              + ("" if done else "，數字尚不完整"))
        return 0
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1, default=str))   # checked: 2026-10-13 會被 YAML 讀成日期
    else:
        sys.stdout.write(markdown(r, c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
