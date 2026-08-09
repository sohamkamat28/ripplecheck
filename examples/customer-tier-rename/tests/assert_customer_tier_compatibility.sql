-- Returns rows only when the compatibility contract is violated.
SELECT *
FROM warehouse.analytics.customer_360
WHERE customer_tier IS DISTINCT FROM loyalty_tier
   OR loyalty_tier IS NULL
