"""Card Pulse: is credit card usage keeping up with issuance?
Reads data.csv (RBI monthly card statistics, Jan-Sep 2026) and prints spend per card and growth.
Run: python analysis.py   (Python 3, no extra packages)"""
import csv, pathlib

here = pathlib.Path(__file__).parent
rows = list(csv.DictReader(open(here / "data.csv")))

print(f"{'Month':<9}{'Cards (mn)':>11}{'Spend (L cr)':>14}{'Spend/card (Rs)':>17}{'Index':>8}")
base = None
for r in rows:
    cards = float(r["cards_outstanding_mn"]) * 1e6
    spend = float(r["spend_inr_lakh_cr"]) * 1e12      # 1 lakh crore = 10^12 rupees
    ppc = spend / cards
    base = base or ppc
    print(f"{r['month']:<9}{cards/1e6:>11.2f}{spend/1e12:>14.2f}{ppc:>17,.0f}{ppc/base*100:>8.1f}")

first, last = rows[0], rows[-1]
cg = float(last["cards_outstanding_mn"]) / float(first["cards_outstanding_mn"]) - 1
print(f"\nCards outstanding growth {first['month']} -> {last['month']}: {cg:+.1%}")

print("\nIssuer spend per card, April 2026")
for r in csv.DictReader(open(here / "issuers_apr2026.csv")):
    ppc = float(r["spend_inr_cr"]) * 1e7 / (float(r["cards_outstanding_mn"]) * 1e6)  # 1 crore = 10^7
    print(f"  {r['issuer']:<12} Rs {ppc:,.0f}  (spend YoY {float(r['spend_yoy_pct']):+.2f}%)")
