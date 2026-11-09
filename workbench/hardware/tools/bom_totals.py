"""Sum a SAO BOM csv: python3 -I bom_totals.py planning-design/rng/bom.csv ...

Counts only rows with qty > 0. Reports verified vs estimated subtotals and the
number of unique extended SMT part types (JLCPCB charges an extended-part
loading fee per unique type; check the current fee, it is not quoted here).
"""
import csv
import sys


def totals(path):
    rows = [r for r in csv.DictReader(open(path)) if int(r["qty"]) > 0]
    out = {"verified_1": 0.0, "est_1": 0.0, "verified_100": 0.0, "est_100": 0.0}
    ext_types = set()
    for r in rows:
        q = int(r["qty"])
        k = "verified" if r["price_status"] == "verified" else "est"
        out[k + "_1"] += q * float(r["unit_1"])
        out[k + "_100"] += q * float(r["unit_100"])
        if r["jlc_class"] == "ext" and r["smt"] == "Y":
            ext_types.add(r["mfr_part"])
    out["total_1"] = out["verified_1"] + out["est_1"]
    out["total_100"] = out["verified_100"] + out["est_100"]
    out["ext_smt_types"] = len(ext_types)
    return out


for p in sys.argv[1:]:
    t = totals(p)
    print(p)
    for k, v in t.items():
        print(f"  {k}: {v:.2f}" if isinstance(v, float) else f"  {k}: {v}")
