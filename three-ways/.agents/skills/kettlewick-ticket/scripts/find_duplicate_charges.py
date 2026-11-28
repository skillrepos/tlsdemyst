"""Find duplicate charges for one Kettlewick order.

Usage: python3 find_duplicate_charges.py charges.csv <order number>
Prints every charge for the order and says whether any look like duplicates
(same order, same day, same amount). Reads the file only; changes nothing.
"""
import csv
import sys
from collections import defaultdict

if len(sys.argv) != 3:
    sys.exit("Usage: python3 find_duplicate_charges.py charges.csv <order number>")

path, order = sys.argv[1], sys.argv[2].strip()
with open(path, newline="") as f:
    rows = [r for r in csv.DictReader(f) if r["order_id"].strip() == order]

if not rows:
    print(f"No charges found for order {order}.")
    sys.exit(0)

print(f"Charges for order {order}:")
for r in rows:
    print(f"  {r['charge_id']}  {r['charge_date']}  ${float(r['amount_usd']):.2f}  {r['status']}")

groups = defaultdict(list)
for r in rows:
    groups[(r["charge_date"], r["amount_usd"])].append(r["charge_id"])

dupes = {k: v for k, v in groups.items() if len(v) > 1}
if not dupes:
    print("No duplicates found.")
for (date, amount), ids in dupes.items():
    extra = len(ids) - 1
    print(f"DUPLICATE: {len(ids)} charges of ${float(amount):.2f} on {date} ({', '.join(ids)}).")
    print(f"  Extra to refund: {extra} x ${float(amount):.2f} = ${extra * float(amount):.2f} (keep {ids[0]}, refund {', '.join(ids[1:])}).")
