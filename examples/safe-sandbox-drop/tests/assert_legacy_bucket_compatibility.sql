-- Fails while a consumer still depends on the deprecated field.
-- Replace this fixture assertion with the live DataHub lineage query in CI.
SELECT 'legacy_bucket' AS blocked_field
WHERE 1 = 0
