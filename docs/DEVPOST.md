# Devpost submission copy

## Project name

Ripplecheck

## Tagline

The DataHub MCP agent that compiles breaking warehouse DDL into a provable, owner-routed migration plan.

## Chosen challenge

**Agents That Do Real Work**

Ripplecheck reads DataHub context, simulates a real change, applies an auditable release policy, creates assigned migration work and code artifacts, and persists its hash-sealed result. Its output is an executable handoff, not a chat answer.

## Short description

Ripplecheck is a counterfactual schema migration compiler. Paste a Snowflake `ALTER TABLE` statement and it uses DataHub MCP to resolve the field, trace exact column-level lineage paths, load owners and criticality, and project which contracts fail without touching production. Stable policy IDs produce a reproducible release gate. The agent then builds a dependency-aware, owner-routed zero-downtime migration DAG and generates a six-file PR pack with compatibility SQL, dbt contract YAML, a parity test, the review decision, owner routing, and a hash-addressed evidence capsule. With writeback enabled, that capsule is appended to the DataHub column for the next engineer or agent.

The complete judge path runs offline with one command, no key, no paid model, and no installation. Live mode speaks MCP over stdio to the official DataHub MCP Server.

## Inspiration

Schema migrations are reviewed as local code changes but fail as graph events. Renaming one warehouse column can invalidate a dbt contract, stop an Airflow task, skew an online ML feature, and silently stale an executive dashboard. DataHub already contains the relationships, governance tags, and owners, yet most tools stop at search, chat, or a blast-radius list.

We wanted DataHub to participate at the exact moment a change is authorized. The key question was not only “what breaks?” but “what must be true before merge, who owns each step, and what artifacts can an agent generate now?”

## What it does

The default demo accepts real DDL:

```sql
ALTER TABLE warehouse.analytics.customer_360
RENAME COLUMN customer_tier TO loyalty_tier;
```

Ripplecheck then:

1. resolves the canonical DataHub entity with `search`;
2. verifies the field, type, documentation, and tags with `list_schema_fields`;
3. traces column lineage through three hops with `get_lineage`;
4. batch-loads owners, asset types, domains, platforms, and criticality with `get_entities`;
5. projects the metadata graph after the proposed rename without mutating production;
6. predicts failure modes and keeps the exact path to each affected consumer;
7. evaluates stable rules `RC-001` through `RC-044` and closes the release gate with evidence;
8. compiles a migration DAG from freeze gate through compatibility, parallel consumer work, convergence proof, and human-approved retirement;
9. generates and downloads a deterministic six-file PR evidence pack;
10. persists the hash-sealed capsule through `update_description`.

The default result finds five broken edges: one dbt model, one Airflow flow, one production ML model, and two dashboards. It identifies three critical consumers, four known owners, one ownership gap, two lineage hops, and four blocking policy failures. The output is stable, inspectable, and reproducible.

## How we built it

The core is a dependency-free Python 3.11 compiler. A constrained parser accepts common Snowflake DDL and natural language. The orchestration layer calls the DataHub MCP tool contract. The counterfactual engine operates on the returned field-and-consumer subgraph; the policy engine emits explicit `PASS`, `WARN`, and `FAIL` evidence; the DAG compiler converts findings into dependency-aware tasks with actors and gates.

The change capsule canonicalizes request, graph, ownership, tag, and policy evidence and signs it with SHA-256. Python's `zipfile` builds deterministic review artifacts in memory with fixed timestamps so identical evidence creates byte-identical output.

There are two DataHub transports. The fixture transport implements the same official tool names over a synthetic retail metadata graph for a credential-free demo. The live transport initializes the official DataHub MCP Server and calls it over JSON-RPC stdio. Both use the same agent path, and live errors never fall back silently.

The agent is available as a responsive web app, JSON API, CLI, and MCP stdio server. Docker, a free-plan Render Blueprint, GitHub Actions, health checks, deterministic samples, and an Apache 2.0 license are included.

## Technical highlights

- Exact lineage paths, not only affected-asset counts.
- Non-mutating before/after graph projection with asset-specific failure modes.
- Stable, auditable policy rule IDs and a measurable gate-open condition.
- Explicit ML feature protection, criticality, reversibility, and ownership-gap rules.
- Owner-routed dependency DAG with parallel consumer migration and human approval.
- Generated compatibility SQL, dbt contracts, and parity tests.
- Deterministic capsule and byte-identical ZIP for reproducible review.
- Hash-sealed DataHub writeback containing affected URNs, owners, blockers, and hashes.
- Zero-cost offline judge path with no model, key, network, or install step.

## Challenges we ran into

### Keeping offline mode honest

A static mock would look impressive but prove little. Both transports therefore share the same orchestration, tool names, graph traversal, policy, writeback, DAG, and artifact-generation code. Checked-in samples are regenerated through the actual compiler path.

### Turning lineage into an action plan

A flat impact list does not express order or accountability. We introduced typed execution nodes with dependencies, actors, states, and evidence. Compatibility work gates parallel consumer migrations; convergence gates final human-approved retirement.

### Making a release decision explainable

An opaque risk probability is difficult to trust. Ripplecheck uses an explicit priority score plus stable rules whose status and evidence are visible. Missing ownership remains a named warning instead of disappearing into a confidence number.

### Producing useful code safely

The agent must help without applying risky changes. Generated SQL, YAML, and tests are packaged for review and never executed. The submitted DDL is also never run; only the metadata graph is projected.

## Accomplishments that we are proud of

- One rename demonstrates warehouse, orchestration, BI, ML, governance, ownership, and writeback in under three minutes.
- The output moves from evidence to assigned work to concrete PR files.
- Every block is tied to a stable rule and exact DataHub path.
- The same evidence always produces the same capsule and ZIP.
- The complete demo is one command and costs zero.
- The project is compact enough for judges to audit but complete enough to deploy.

## What we learned

Metadata becomes operational when it is paired with a decision boundary and a handoff. Lineage says where risk travels; ownership says who can resolve it; tags say which rules apply; writeback gives the organization shared memory. DataHub MCP makes those pieces available in one agent workflow.

We also learned that deterministic authority and generative assistance should be separated. A model can improve ergonomics, but a production release gate should remain reproducible from metadata evidence.

## What's next

- Trigger Ripplecheck on warehouse and dbt migration pull requests.
- Emit GitHub Check annotations and attach the PR pack automatically.
- Refresh DataHub lineage after each consumer migration and update DAG node state.
- Write structured DataHub properties when a shared capsule schema is available.
- Add policy packs for PII, finance, SLA, and regional residency changes.
- Add optional local-model parsing while preserving deterministic release authority.
- Publish the schema-migration compiler as a reusable DataHub skill.

## Built with

- DataHub MCP Server tool contract
- Model Context Protocol over JSON-RPC stdio
- Python 3.11 standard library
- SHA-256 and deterministic ZIP generation
- Semantic HTML, CSS, and vanilla JavaScript
- Docker, Render Blueprints, and GitHub Actions

## Links to paste before submission

- **Public repository:** `https://github.com/sohamkamat28/ripplecheck`
- **Project URL:** `https://github.com/sohamkamat28/ripplecheck` (the host permits a repository with clear setup instructions; replace only with a verified hosted URL)
- **Sample outputs:** `https://github.com/sohamkamat28/ripplecheck/tree/main/examples`
- **Demo video:** `https://youtu.be/<your-video-id>`

## Suggested Devpost tags

`datahub`, `mcp`, `metadata`, `data-lineage`, `schema-migration`, `data-governance`, `developer-tools`, `mlops`, `python`

## Judging alignment

| Criterion | Evidence |
| --- | --- |
| Use of DataHub | Five-call MCP loop across schema, lineage, owners, tags, and hash-sealed writeback |
| Technical execution | Counterfactual graph, stable policy proof, execution DAG, deterministic artifacts, web/CLI/MCP, tests, CI, Docker, and live transport |
| Originality | Compiles a schema change into release evidence and migration code instead of providing catalog chat or a flat blast radius |
| Real-world usefulness | Prevents known data and ML breakage, sequences a reversible rollout, and routes every consumer to an owner |
| Submission quality | One-command zero-cost demo, exact runbook, public-repo package, checked-in samples, deploy config, and under-three-minute script |

## Final submission check

The deadline is **August 10, 2026 at 5:00 PM EDT**, or **August 11 at 2:30 AM IST**. Add the video URL, run `make samples && make verify`, confirm every URL in an incognito window, and follow `docs/DEMO_RUNBOOK.md` for the recording. Use `docs/DEVPOST_FORM.md` for every live submission field.
