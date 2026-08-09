# Ripplecheck release decision

**Capsule:** `RC-4AC01328A4AA`  
**Decision:** `BLOCK`  
**Release gate:** `CLOSED`  
**Proposed change:** `ALTER TABLE warehouse.analytics.customer_360 RENAME COLUMN customer_tier TO loyalty_tier;`

## Why

Block the change. Renaming customer_tier impacts 5 assets.

## Policy proof

- `RC-001` **FAIL**: 5 active column-lineage edges found across the inspected graph.
- `RC-007` **FAIL**: 3 affected assets carry the Critical tag.
- `RC-013` **WARN**: 1 affected asset has no DataHub owner.
- `RC-021` **FAIL**: 1 production ML consumer uses the proposed field.
- `RC-032` **FAIL**: Direct DDL has no compatibility window or rollback gate.
- `RC-044` **PASS**: DataHub evidence loaded for tags: Critical, Tier1.

## Lineage evidence

- `warehouse.analytics.customer_360 -> airflow.customer_segmentation`
- `warehouse.analytics.customer_360 -> dbt.marts.customer_retention`
- `warehouse.analytics.customer_360 -> mlflow.churn_risk_v3`
- `warehouse.analytics.customer_360 -> dbt.marts.customer_retention -> looker.executive_growth`
- `warehouse.analytics.customer_360 -> dbt.marts.customer_retention -> tableau.retention_operations`

## Release condition

Migrate every active consumer, reach 100% ownership, and rerun this capsule.

Generated deterministically from the DataHub MCP evidence path.
