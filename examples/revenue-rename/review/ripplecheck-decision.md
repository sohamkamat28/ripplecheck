# Ripplecheck release decision

**Capsule:** `RC-DAE79F33A169`  
**Decision:** `BLOCK`  
**Release gate:** `CLOSED`  
**Proposed change:** `ALTER TABLE warehouse.finance.monthly_revenue RENAME COLUMN net_revenue TO recognized_revenue;`

## Why

Block the change. Renaming net_revenue impacts 1 assets.

## Policy proof

- `RC-001` **FAIL**: 1 active column-lineage edges found across the inspected graph.
- `RC-007` **FAIL**: 1 affected assets carry the Critical tag.
- `RC-013` **PASS**: 0 affected assets have no DataHub owner.
- `RC-021` **PASS**: 0 production ML consumer uses the proposed field.
- `RC-032` **FAIL**: Direct DDL has no compatibility window or rollback gate.
- `RC-044` **PASS**: DataHub evidence loaded for tags: Critical, Financial.

## Lineage evidence

- `warehouse.finance.monthly_revenue -> looker.finance_close`

## Release condition

Migrate every active consumer, reach 100% ownership, and rerun this capsule.

Generated deterministically from the DataHub MCP evidence path.
