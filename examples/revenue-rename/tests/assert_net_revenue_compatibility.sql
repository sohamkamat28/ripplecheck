-- Returns rows only when the compatibility contract is violated.
SELECT *
FROM warehouse.finance.monthly_revenue
WHERE net_revenue IS DISTINCT FROM recognized_revenue
   OR recognized_revenue IS NULL
