"""scripts/cost.py 對 tests/cost-fixture.yaml 的手算核對。python3 -m unittest discover tests"""
import copy
import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import cost  # noqa: E402

FIXTURE = yaml.safe_load((Path(__file__).parent / "cost-fixture.yaml").read_text(encoding="utf-8"))


class CostTest(unittest.TestCase):
    def setUp(self):
        self.c = copy.deepcopy(FIXTURE)
        self.assertEqual(cost.validate(self.c), [])

    def test_kwh_and_cooling(self):
        r = cost.compute(self.c)
        kwh = {d["name"]: d["kwh_per_month"] for d in r["devices"]}
        # 一個月 365/12 天：A 2×50 W×24 h = 73.0 度，B 100 W×12 h = 36.5，F 10 W = 7.3
        # 冷氣：熱負載 100 + 100×12/24 + 10 = 160 W，除以 COP 4 = 40 W，29.2 度
        self.assertAlmostEqual(kwh["A"], 73.0)
        self.assertAlmostEqual(kwh["B"], 36.5)
        self.assertAlmostEqual(kwh["F"], 7.3)
        self.assertAlmostEqual(kwh["AC"], 29.2)
        self.assertAlmostEqual(r["kwh_per_month_total"], 146.0)

    def test_tiered_marginal(self):
        r = cost.compute(self.c)
        # 300 到 446 度：330 以下 30 度，331 到 500 116 度
        # 非夏季 30×2.26 + 116×3.13 = 430.88，夏季 30×2.55 + 116×3.80 = 517.30
        # 一年 4×517.30 + 8×430.88 = 5,516.24
        self.assertAlmostEqual(r["electricity_per_year"], 5516.24)

    def test_amortization(self):
        r = cost.compute(self.c)
        am = {d["name"]: d["amortization_per_year"] for d in r["devices"]}
        self.assertAlmostEqual(am["A"], 50000)       # 2×100,000 / 4
        self.assertAlmostEqual(am["B"], 3000)        # (20,000 − 5,000) / 5
        self.assertAlmostEqual(am["F"], 1200)        # 年費
        self.assertAlmostEqual(r["amortization_per_year"], 54200)
        self.assertFalse(r["incomplete"])
        self.assertAlmostEqual(r["onprem_per_year"], 5516.24 + 54200)

    def test_breakeven_only_replaced(self):
        r = cost.compute(self.c)
        busy, always = r["comparisons"][0], r["comparisons"][1]
        self.assertEqual(busy["replaced"], ["A"])
        # 拿掉 A 剩 73 度：300 到 373，非夏季 30×2.26 + 43×3.13 = 202.39，夏季 76.5 + 43×3.80 = 239.9
        # 一年 4×239.9 + 8×202.39 = 2,578.72，省下 5,516.24 − 2,578.72 = 2,937.52
        self.assertAlmostEqual(busy["replaced_electricity_per_year"], 2937.52)
        self.assertAlmostEqual(busy["replaced_onprem_per_year"], 2937.52 + 50000)
        # busy：(10×5 + 5)×30 = 1,650 元/月，一年 19,800，回本 200,000 / ((19,800 − 2,937.52)/12)
        self.assertAlmostEqual(busy["cloud_per_year"], 19800)
        self.assertAlmostEqual(busy["breakeven_months"], 200000 / ((19800 - 2937.52) / 12))
        # always：(10×730 + 5)×30 = 219,150 元/月
        self.assertAlmostEqual(always["cloud_per_year"], 219150 * 12)
        self.assertAlmostEqual(always["breakeven_months"], 200000 / ((219150 * 12 - 2937.52) / 12))

    def test_base_scenarios(self):
        r = cost.compute(self.c)
        # 基礎度數有填：對照只用它，電費的敏感度表仍列情境
        self.assertEqual([(x["household_base_kwh_per_month"], x["scenario"]) for x in r["comparisons"]],
                         [(300, "busy"), (300, "always")])
        self.assertEqual([b["household_base_kwh_per_month"] for b in r["by_base"]], [300, 900])
        self.c["tariff"]["household_base_kwh_per_month"] = None
        r = cost.compute(self.c)
        self.assertEqual([(x["household_base_kwh_per_month"], x["scenario"]) for x in r["comparisons"]],
                         [(300, "busy"), (300, "always"), (900, "busy"), (900, "always")])
        # 900 到 1,046 度：1000 以下 100 度，以上 46 度
        e = 4 * (100 * 6.44 + 46 * 8.86) + 8 * (100 * 5.27 + 46 * 7.03)
        self.assertAlmostEqual(cost.elec_year(146.0, 900, self.c["tariff"]), e)

    def test_by_base_and_partial_flags(self):
        self.c["tariff"]["household_base_kwh_per_month"] = None
        r = cost.compute(self.c)
        self.assertIsNone(r["electricity_per_year"])
        self.assertFalse(r["missing_kwh"])
        self.assertFalse(r["missing_amortization"])
        self.assertEqual([b["household_base_kwh_per_month"] for b in r["by_base"]], [300, 900])
        self.assertAlmostEqual(r["by_base"][0]["electricity_per_year"], 5516.24)
        self.assertAlmostEqual(r["by_base"][0]["onprem_per_year"], 5516.24 + 54200)
        out = cost.markdown(r, self.c)
        self.assertNotIn("（不含待填）", out)     # 度數與攤提都齊，只差基礎度數

    def test_never_pays_back(self):
        self.c["cloud"]["items"] = [{"name": "便宜", "replaces": ["A"], "monthly_twd": 100, "source": "x"}]
        self.c["cloud"]["scenarios"] = []
        cmp = cost.compute(self.c)["comparisons"][0]
        self.assertTrue(cmp["never_pays_back"])
        self.assertIn("不會回本", cost.markdown(cost.compute(self.c), self.c))

    def test_missing_marks_incomplete(self):
        self.c["tariff"]["household_base_kwh_per_month"] = None
        self.c["devices"][1]["watts_avg"] = None
        r = cost.compute(self.c)
        self.assertTrue(r["incomplete"])
        self.assertTrue(r["missing_kwh"])
        self.assertIsNone(r["electricity_per_year"])
        self.assertIsNone(r["comparisons"][0]["replaced_electricity_per_year"])
        out = cost.markdown(r, self.c)
        self.assertIn("（不含待填）", out)
        self.assertIn(cost.MISSING, out)
        # B 沒有瓦數時冷氣也推不出來
        self.assertIsNone({d["name"]: d for d in r["devices"]}["AC"]["watts_avg"])

    def test_json_with_date(self):
        import datetime, io, contextlib
        self.c["cloud"]["items"][0]["checked"] = datetime.date(2026, 10, 13)   # YAML 讀到的樣子
        p = Path(__file__).parent / ".tmp-cost.yaml"
        p.write_text(yaml.safe_dump(self.c, allow_unicode=True), encoding="utf-8")
        try:
            buf = io.StringIO()
            sys.argv = ["cost.py", "--file", str(p), "--json"]
            with contextlib.redirect_stdout(buf):
                self.assertEqual(cost.main(), 0)
            self.assertIn('"checked": "2026-10-13"', buf.getvalue())
        finally:
            p.unlink()

    def test_watts_label(self):
        self.c["devices"][0]["watts_label"] = "實測（插座逐日）"
        r = cost.compute(self.c)
        src = {d["name"]: d["watts_source"] for d in r["devices"]}
        self.assertEqual(src["A"], "實測（插座逐日）")   # 有 label 用 label
        self.assertEqual(src["B"], "規格值")             # 沒有就用 watts_source 的中文
        self.assertEqual(src["AC"], "推得")
        self.c["devices"][0]["watts_label"] = 3
        self.assertIn("watts_label", "\n".join(cost.validate(self.c)))

    def test_flat(self):
        self.c["tariff"] = {"kind": "flat", "flat_twd_per_kwh": 4.0}
        self.assertEqual(cost.validate(self.c), [])
        self.assertAlmostEqual(cost.compute(self.c)["electricity_per_year"], 146.0 * 12 * 4.0)

    def test_validate_rejects(self):
        self.c["cloud"]["items"][0]["replaces"] = ["不存在"]
        self.c["cloud"]["items"][0]["hours_per_month"] = {"busy": 5}
        self.c["devices"][0]["watts_source"] = "猜的"
        errs = "\n".join(cost.validate(self.c))
        self.assertIn("不存在的設備", errs)
        self.assertIn("情境要與 cloud.scenarios 一致", errs)
        self.assertIn("watts_source", errs)


if __name__ == "__main__":
    unittest.main()
