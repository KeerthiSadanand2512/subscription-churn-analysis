"""Generate a fictional subscription history and run the SQL analysis."""
import csv
import random
import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parent
rng = random.Random(42)
snapshot = 18  # Exclusive end of the observation window.
plans = {"Monthly": 0.09, "Annual": 0.035}
rows = []
for customer in range(1, 2401):
    signup = rng.randrange(12)
    plan = rng.choice(list(plans))
    churn = None
    for age in range(1, snapshot - signup):
        # Annual subscriptions can end at their renewal boundary.
        if plan == "Annual" and age % 12:
            continue
        if rng.random() < plans[plan]:
            churn = signup + age
            break
    rows.append((customer, signup, plan, churn))

with sqlite3.connect(":memory:") as db:
    db.execute("""CREATE TABLE subscriptions (
        customer_id INTEGER PRIMARY KEY, signup_month INTEGER NOT NULL,
        plan TEXT NOT NULL, churn_month INTEGER
    )""")
    db.executemany("INSERT INTO subscriptions VALUES (?, ?, ?, ?)", rows)
    db.execute("CREATE TABLE observation (end_month INTEGER NOT NULL)")
    db.execute("INSERT INTO observation VALUES (?)", (snapshot,))
    assert db.execute("""SELECT COUNT(*) FROM subscriptions
        WHERE churn_month <= signup_month OR churn_month >= ?""", (snapshot,)).fetchone()[0] == 0
    result = db.execute((root / "sql/retention.sql").read_text())
    columns = [field[0] for field in result.description]
    results = result.fetchall()
    assert all(0 <= active <= size and size == lost + active for _, _, _, size, lost, active, _ in results)
    with (root / "reports/retention.csv").open("w", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(results)
    print(f"Analyzed {len(rows):,} subscriptions and wrote {len(results)} cohort results.")
