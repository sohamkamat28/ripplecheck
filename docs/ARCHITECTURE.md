# Architecture and agent contract

## Goal

Given proposed warehouse DDL, Ripplecheck answers a bounded operational question: **what must be true before this schema change can merge, and what review-ready work can be compiled from DataHub evidence now?**

It never executes the submitted DDL.

## Input

The default public input is real Snowflake DDL:

```sql
ALTER TABLE warehouse.analytics.customer_360
RENAME COLUMN customer_tier TO loyalty_tier;
```

The constrained parser accepts DDL for drop, rename, and type change plus plain-language drop, rename, type change, and deprecation. It returns a stable `ChangeRequest`; unknown syntax stops rather than guessing.

## Evidence sequence

| Order | DataHub MCP tool | Evidence gathered | Compiler consumer |
| --- | --- | --- | --- |
| 1 | `search` | Canonical entity and URN | Source resolution |
| 2 | `list_schema_fields` | Field existence, type, tags, description | Before-state and governed-field policy |
| 3 | `get_lineage` | Column consumers and paths over 3 hops | Broken-edge projection and failure modes |
| 4 | `get_entities` | Owners, platforms, domains, types, criticality | Routing, ownership coverage, ML and dashboard rules |
| 5 | `update_description` | Mutation response | Hash-sealed decision capsule persisted to the source column |

The first four calls are read-only. The fifth is gated by the web checkbox, CLI flag, MCP argument, and DataHub's `TOOLS_IS_MUTATION_ENABLED` setting.

## Compilation stages

```text
parse -> resolve -> verify -> traverse -> enrich
      -> counterfactual -> policy proof -> release gate
      -> execution DAG -> hash-sealed writeback -> PR evidence pack
```

### Counterfactual projection

The compiler clones the relevant field-and-consumer subgraph in memory and applies the requested semantic diff. It emits:

- before and projected field state;
- broken consumer edges;
- exact source-to-consumer paths;
- asset-specific failure modes;
- critical consumer count;
- maximum lineage depth;
- ownership coverage and gaps.

The projection is deterministic and non-mutating.

### Stable policy proof

| Rule | Invariant | Blocking behavior |
| --- | --- | --- |
| `RC-001` | Breaking changes need zero active consumers | Fails on an active lineage edge |
| `RC-007` | Critical consumers require explicit migration | Fails on a Critical downstream asset |
| `RC-013` | Every affected asset needs an accountable owner | Warns on missing ownership |
| `RC-021` | Production ML inputs need feature migration | Fails on a Production ML consumer |
| `RC-032` | Rollout must be backward compatible and reversible | Fails direct breaking DDL with active consumers |
| `RC-044` | Governed fields require catalog evidence | Passes only after schema/tag evidence is loaded |

The public `BLOCK`, `REVIEW`, or `SAFE` decision remains a compact summary. The release gate is `CLOSED` whenever failed rules exist and `OPEN` only when evidence satisfies the bounded policy.

### Execution DAG

The default rename produces dependency-aware work:

1. `G0`: freeze direct DDL;
2. `M1`: introduce the replacement field;
3. `M2`: publish the dual-read compatibility layer;
4. `C1..Cn`: migrate consumers in parallel, routed to DataHub owners;
5. `V1`: prove contract parity and refreshed lineage convergence;
6. `G1`: require human approval before retiring the old field.

Every node has an ID, dependency list, accountable actor, state, and evidence.

### Change capsule

The capsule contains:

- canonicalized request and source identity;
- policy statuses and gate state;
- compiler and schema version;
- SHA-256 of canonical input evidence;
- SHA-256 of the lineage/ownership/tag graph evidence;
- catalog snapshot and transport provenance.

The same evidence produces the same capsule and byte-identical ZIP.

## Output contract

Each assessment returns:

- parsed request, source, field, decision, and explainable risk;
- ordered blast radius with exact lineage paths;
- counterfactual before/after state and predicted failures;
- stable policy proof and release gate;
- owner-routed execution DAG;
- artifact manifest and deterministic change capsule;
- complete MCP trace;
- hash-sealed writeback status.

The in-memory ZIP endpoint compiles six concrete files: compatibility SQL, dbt contract YAML, parity SQL, PR decision Markdown, owner-routing JSON, and the capsule manifest.

## Offline and live transports

`FixtureDataHubTools` implements the official tool names over `data/catalog.json`. It provides the entire judge path without credentials, network, billing, or an 8 GB DataHub quickstart. Demo writebacks are recorded in gitignored `data/run-state.json` and reapplied to the in-memory column description.

`StdioMCPDataHubTools` launches the official `uvx mcp-server-datahub@latest` package, completes the MCP initialize handshake, and calls the same names over JSON-RPC stdio. `DATAHUB_GMS_URL` and `DATAHUB_GMS_TOKEN` point it at DataHub OSS or Cloud; `RIPPLECHECK_MODE=live` selects it. Live failures include the server's diagnostic tail and never fall back silently to fixtures.

## Safety properties

- Submitted DDL is parsed but never executed.
- Missing datasets, fields, and unsupported syntax stop the compiler.
- The graph projection does not mutate DataHub.
- Writeback is explicit and independently disableable.
- Generated code is a review artifact and is never applied automatically.
- The HTTP server rejects bodies larger than 32 KB and prevents static path traversal.
- Download tokens are deterministic run IDs held only in process memory.
- The release decision is deterministic policy, not an LLM probability.

## Why no paid model

Release authority benefits from reproducibility. The core path therefore uses deterministic parsing, metadata evidence, policies, and artifact generation. This removes cost and makes judging repeatable while retaining an agentic loop: interpret, gather context, simulate, decide, assign, act, persist, and hand off. A local or hosted model can later broaden parsing and remediation suggestions without overriding the evidence gate.
