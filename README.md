# Subscription churn analysis

How many subscribers are still active 1, 3, 6, and 12 months after signup? This project uses SQLite to answer that question for monthly and annual plans across 12 signup cohorts.

## Run the analysis

Run `python3 run.py` from the project folder. It uses Python's standard library, generates 2,400 fictional subscriptions, runs [the retention query](sql/retention.sql), and writes [the cohort results](reports/retention.csv).

## How retention is measured

A cohort is a group of customers who signed up in the same month on the same plan. Retention at month N is the share of the original cohort whose subscription has yet to end at that age. Cancellations effective at month N count as churn at that horizon. The query includes a cohort only when the full horizon falls inside the observation window.

## What the simulation shows

At month 12, 566 of 582 annual subscribers (97.25%) and 173 of 586 monthly subscribers (29.52%) were still active across the six eligible signup months. These are customer-weighted rates calculated from the underlying counts. The generator gives monthly plans a 9% cancellation probability each month and annual plans a 3.5% probability at renewal. Those assumptions explain the gap. The analysis demonstrates how to measure retention with different renewal schedules. Estimating the effect of plan choice would require real subscription histories and a design that accounts for differences between customers who choose each plan.
