-- Retention at fixed subscription ages, restricted to observable cohorts.
WITH horizons(age_months) AS (
    VALUES (1), (3), (6), (12)
),
eligible AS (
    SELECT s.signup_month, s.plan, h.age_months,
           CASE WHEN s.churn_month <= s.signup_month + h.age_months
                THEN 1 ELSE 0 END AS churned
    FROM subscriptions AS s
    CROSS JOIN horizons AS h
    CROSS JOIN observation AS o
    WHERE s.signup_month + h.age_months < o.end_month
)
SELECT signup_month, plan, age_months,
       COUNT(*) AS cohort_size,
       SUM(churned) AS churned_customers,
       COUNT(*) - SUM(churned) AS active_customers,
       ROUND(100.0 * (COUNT(*) - SUM(churned)) / COUNT(*), 2) AS retention_pct
FROM eligible
GROUP BY signup_month, plan, age_months
ORDER BY signup_month, plan, age_months;
