# Verified DataHub OSS + MCP run

This is the reproducible evidence that Ripplecheck is not only a hard-coded interface. On August 10, 2026, the same agent path used by the offline judge demo completed an end-to-end run against a real local DataHub catalog through the official DataHub MCP Server.

## Verified stack

| Component | Verified value |
| --- | --- |
| Catalog | DataHub OSS Docker Quickstart 1.6.0 |
| Catalog data | Official `showcase-ecommerce` DataHub datapack |
| MCP server | Official `mcp-server-datahub`, launched with `uvx mcp-server-datahub@latest` |
| MCP transport | JSON-RPC over stdio |
| Agent transport | `RIPPLECHECK_MODE=live`; no fixture fallback |
| Write permission | MCP mutation tools explicitly enabled for the local test |

The quickstart started its full local stack successfully, and the official datapack ingested 10 definition events, 3,562 data events, and 54 document events. Ripplecheck then initialized the MCP server, used its returned payloads, and normalized those official response envelopes at the transport boundary.

## Exact live assessment

Proposed warehouse change:

```sql
ALTER TABLE b2fd91.order_entry_db.analytics.order_details
RENAME COLUMN order_id TO order_identifier;
```

Observed result:

| Evidence | Actual result |
| --- | --- |
| Decision | `BLOCK` |
| Risk | `10/10` |
| Downstream assets | 23 |
| Maximum returned lineage degree | 4 |
| Critical consumers | 1 |
| Ownership coverage | 52% |
| Release gate | `CLOSED` |
| Generated PR files | 6 |

The read-only run called, in order:

1. `search`
2. `list_schema_fields`
3. `get_lineage`
4. `get_entities`

The writeback run called the same four tools and then `update_description`. The official MCP mutation returned:

```json
{
  "success": true,
  "urn": "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)",
  "column_path": "order_id",
  "message": "Description updated successfully"
}
```

The checked-in machine-readable summary is [`samples/live-datahub-proof.json`](../samples/live-datahub-proof.json). It contains no token, credential, or private catalog data.

## Reproduce on a local DataHub

DataHub's current local quickstart requires Docker and substantially more resources than the dependency-free fixture demo. Follow the official [DataHub Quickstart](https://docs.datahub.com/docs/quickstart) and [DataHub MCP guide](https://docs.datahub.com/docs/features/feature-guides/mcp), then run:

```bash
datahub docker quickstart --version v1.6.0
datahub init
datahub datapack load showcase-ecommerce

export DATAHUB_GMS_URL="http://localhost:8080"
export DATAHUB_GMS_TOKEN="<your-local-datahub-token>"
export RIPPLECHECK_MODE=live
export DATAHUB_MCP_COMMAND="uvx mcp-server-datahub@latest"
export TOOLS_IS_MUTATION_ENABLED=true

python3 main.py web --host 127.0.0.1 --port 8000
```

Use a real personal access token on an authenticated instance. The 1.6.0 quickstart used for this proof had metadata-service authentication disabled in its generated compose environment; its local MCP test therefore accepted a non-secret placeholder value for the required token variable. No placeholder token is committed here.

## Safety and judge path

- Ripplecheck never executes the submitted DDL.
- Disable writeback in the interface, or unset `TOOLS_IS_MUTATION_ENABLED`, for read-only use.
- Live failures are surfaced and never fall back silently to the fixture.
- The default judge demo remains the small offline snapshot so evaluation needs no Docker, account, token, network, or paid billing.
- Both modes run the same parser, orchestration, counterfactual engine, policy proof, execution-DAG compiler, and artifact generator; only the DataHub transport changes.

