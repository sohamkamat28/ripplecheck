# Ripplecheck demo runbook

This is the single recording document. It contains the exact URL, setup, click path, spoken script, expected screen state, technical talking points, and stack table.

**Target runtime:** 2 minutes 56 seconds  
**Primary challenge:** **Agents That Do Real Work**  
**Demo URL:** [https://ripplecheck-datahub.vercel.app](https://ripplecheck-datahub.vercel.app)
**Cost:** $0. No OpenAI key, DataHub account, paid service, or paid model is needed for the recorded path.

## The winning use case

Ripplecheck is a **counterfactual schema migration compiler**. It does not stop at answering “what breaks?” It takes real warehouse DDL, queries the DataHub MCP graph, projects the after-state without mutating production, proves a bounded release policy, builds an owner-routed zero-downtime execution DAG, persists a hash-sealed decision capsule, and compiles a six-file PR pack.

The default scenario is deliberately cross-functional:

```sql
ALTER TABLE warehouse.analytics.customer_360
RENAME COLUMN customer_tier TO loyalty_tier;
```

One rename crosses a dbt contract, an Airflow flow, a production ML feature, two dashboards, four known owners, and one ownership gap. That lets the demo prove lineage depth, governance, operational routing, ML risk, reversibility, and writeback in one run.

## Pre-recording setup

Open the public production demo:

[https://ripplecheck-datahub.vercel.app](https://ripplecheck-datahub.vercel.app)

If internet access is unreliable during recording, run this local fallback from the repository root:

```bash
python3 main.py web --host 127.0.0.1 --port 8765
```

Then:

1. Open the production URL above, or [http://127.0.0.1:8765](http://127.0.0.1:8765) only as the offline fallback.
2. Record at 1920x1080 and set browser zoom to 80%.
3. Hide bookmarks, downloads, notifications, and personal browser chrome.
4. Refresh once. Confirm the header says **Offline graph ready**.
5. Leave the default DDL unchanged and the **Persist the hash-sealed decision capsule to DataHub** checkbox checked.
6. Do one private rehearsal. Refresh again before the real take so the compiler starts idle.

If port 8000 is occupied, stop that local process and rerun the command. Do not change the URL during recording.

## Click map

| Order | Control text | Exact location | What must appear |
| --- | --- | --- | --- |
| 1 | **Compile migration plan** | Vermilion button in the left **Proposed DDL** pane, below the checked writeback option | **Release gate CLOSED**, 10/10 risk, four metrics, and the **Counterfactual** tab |
| 2 | **Policy proof** | Second tab below the four metric cards in **02 / Release evidence** | Six stable rule IDs, including `RC-001`, `RC-021`, and `RC-032` |
| 3 | **Execution DAG** | Third tab in the same tab row | Nodes `G0` through `G1`, dependencies, states, and accountable actors |
| 4 | **MCP trace** | Fourth tab in the same tab row | Five exact DataHub MCP calls and the hash-sealed writeback result |
| 5 | **Download PR pack (.zip)** | Vermilion button at the bottom-right of **Merge-ready evidence pack** | A ZIP download whose name begins `ripplecheck-rc-4ac01328a4aa` |

Optional after the take: **Copy PR decision** sits directly left of the download button and copies the capsule, gate, blockers, and release condition for a pull request comment.

## Exact click-and-say script

### 0:00-0:17 | Hook

**Screen:** Start at the top on **Compile the change before it compiles you.** Keep the hero and its orange action visible. Do not click yet.

**Say:**

"A warehouse rename can pass code review and still break a dbt contract, a production feature, and an executive dashboard. DataHub knows the relationships. Ripplecheck turns them into a merge-ready migration plan before the DDL touches production."

### 0:17-0:36 | Establish the real change

**Screen:** Click the hero **Compile migration plan** link or scroll once to the workspace. Point to the DDL in the left pane, then point to the checked writeback option.

**Say:**

"This is real Snowflake DDL renaming `customer_tier` to `loyalty_tier` on our canonical customer table. The judge path is fully offline and costs zero, but it uses the same official DataHub MCP tool contract as live mode."

### 0:36-0:59 | Compile

**Click:** **Compile migration plan**, the vermilion button in the left pane. Wait for **Release gate CLOSED**. If needed, scroll just enough to align **Release evidence** with the top of the window.

**Say:**

"I will compile, not execute, the change. Ripplecheck resolves the entity, verifies the field and tags, traces column lineage through three hops, batch-loads owners and criticality, and writes a hash-sealed decision capsule back to DataHub. The direct rename is blocked with a ten out of ten risk score."

### 0:59-1:24 | Show the counterfactual

**Screen:** Stay on the default **Counterfactual** tab. Move the pointer across the before and projected states, then the failure cards. Do not click a card.

**Say:**

"The non-mutating graph projection finds five broken edges: an Airflow transformation, a dbt model, a production churn model, and two dashboards. It preserves the exact path to each failure. Four assets are owner-routed, while DataHub exposes one unowned operational dashboard, so coverage is only eighty percent."

### 1:24-1:47 | Prove the gate

**Click:** **Policy proof**, the second tab below the metrics.

**Say:**

"Every decision is explainable. Stable rules fail active-consumer safety, critical-consumer migration, production ML protection, and reversibility. Ownership is a warning, not hidden uncertainty. The gate states the measurable exit condition: migrate every consumer, reach full ownership, and rerun the capsule."

### 1:47-2:13 | Show work, not advice

**Click:** **Execution DAG**, the third tab. Move the pointer from `G0` down toward `G1`.

**Say:**

"Ripplecheck then converts evidence into work. This dependency graph freezes the direct DDL, introduces the new field, publishes a dual-read compatibility layer, routes each consumer to its DataHub owner, proves parity and lineage convergence, and requires human approval before retiring the old field."

### 2:13-2:34 | Prove DataHub MCP usage

**Click:** **MCP trace**, the fourth tab.

**Say:**

"The provenance is inspectable: `search`, `list_schema_fields`, `get_lineage`, `get_entities`, and `update_description`, with exact arguments. There is no opaque model score and no silent fallback. The same deterministic compiler is exposed through the web app, CLI, and its own MCP server."

### 2:34-2:56 | Ship the handoff

**Screen:** Scroll to **Merge-ready evidence pack** if it is not visible. Point across the six files, then click **Download PR pack (.zip)** at the bottom-right.

**Say:**

"Finally, this is not just a report. The downloadable PR pack contains compatibility SQL, a dbt contract patch, a parity test, the review decision, owner routing, and a hash-addressed change capsule. Ripplecheck makes DataHub an active, auditable release gate, and the complete Apache 2.0 demo runs with one command."

Stop recording immediately after the download begins.

## Tech stack

| Layer | Technology | Why it is used | What it delivers |
| --- | --- | --- | --- |
| Metadata context | DataHub MCP tool contract | DataHub already holds schema, column lineage, tags, owners, domains, and descriptions | Grounded evidence across `search`, `list_schema_fields`, `get_lineage`, `get_entities`, and `update_description` |
| Live integration | Official DataHub MCP Server over JSON-RPC stdio | Keeps the live boundary standards-based and swappable | Real DataHub Cloud or OSS access without changing agent orchestration |
| Offline integration | Synthetic DataHub graph fixture in JSON | Removes credentials, billing, network, and judge setup risk while preserving official tool semantics | Instant, repeatable demo with real graph traversal and durable local writeback |
| Agent orchestration | Python 3.11 standard library | Small attack surface, zero install, transparent control flow | Entity resolution, schema verification, three-hop lineage, batch enrichment, and writeback |
| Counterfactual engine | Deterministic metadata-graph projection | A release gate needs reproducible evidence instead of free-form guesses | Before/after field state, broken edges, exact failure paths, hop depth, and ownership coverage |
| Policy engine | Stable rules `RC-001` through `RC-044` | Rule IDs are reviewable, testable, and CI-compatible | `PASS`, `WARN`, or `FAIL` evidence plus a measurable gate-open condition |
| Migration compiler | Dependency DAG with gates, actors, and prerequisites | Blast-radius lists do not assign or sequence remediation work | Zero-downtime dual-read rollout from freeze gate `G0` to retirement approval `G1` |
| Evidence packaging | Python `zipfile`, canonical JSON, SHA-256 | Reviewers need portable artifacts and tamper-evident provenance | Six-file PR pack and deterministic capsule/evidence hashes |
| Demo API | `ThreadingHTTPServer` and JSON endpoints | Avoids framework installation and keeps the one-command path reliable | Static UI, analysis API, health check, scenarios, and ZIP download |
| Interface | Semantic HTML, modern CSS, vanilla JavaScript | Fast load, no build step, easy public-repo audit | Responsive tabbed evidence console, keyboard navigation, copy action, and download |
| Distribution | Vercel Services, Docker, Render Blueprint, `Procfile` | Gives judges public, serverless, local, and container launch paths | Verified free production URL plus portable deployment options |
| Verification | `unittest`, browser interaction checks, GitHub Actions, preflight script | Submission failures are often packaging or UI failures | Policy, MCP, parser, determinism, ZIP, responsive, and required-file coverage |

## Architecture you can explain if a judge asks

```text
Snowflake DDL
    -> Ripplecheck parser
    -> DataHub MCP evidence calls
    -> non-mutating graph projection
    -> stable policy proof
    -> release gate + owner-routed DAG
    -> DataHub hash-sealed writeback
    -> downloadable PR evidence pack
```

The system is intentionally hybrid: DataHub MCP provides dynamic metadata truth; the compiler and policy are deterministic. A model can later broaden parsing or remediation suggestions without gaining authority over the release gate.

## Expected default result

| Signal | Expected value |
| --- | --- |
| Capsule | `RC-4AC01328A4AA` |
| Decision | `BLOCK` |
| Release gate | `CLOSED` |
| Risk | `10/10` |
| Broken edges | `5` |
| Critical consumers | `3` |
| Owner coverage | `80%` or `4/5` |
| Maximum lineage depth | `2` hops |
| Failed rules | `RC-001`, `RC-007`, `RC-021`, `RC-032` |
| Warning | `RC-013` ownership gap |
| MCP calls | `5` |
| Generated files | `6` |

## Recovery during recording

- If the hosted result does not appear, refresh once. If the network is unstable, switch to the local fallback, confirm the terminal says `Ripplecheck demo listening on http://127.0.0.1:8765`, and restart the take.
- If you accidentally choose another fixture, click **Rename a production contract** under **Judge paths**, then compile again.
- If the browser download is blocked, do not troubleshoot on camera. Point to the six generated files and finish the closing line; the ZIP endpoint is already proven by the test suite.
- If you lose your place, the tab order is always **Counterfactual**, **Policy proof**, **Execution DAG**, **MCP trace**.
- Never enter a key or sign in during the video. The winning path is explicitly offline.

## Final upload check

- Runtime is below 3:00.
- The URL, DDL, gate status, rule IDs, MCP calls, and artifact names are readable at 1080p.
- Captions are enabled.
- Video visibility is public or unlisted.
- The public repository, live demo, and video links have replaced the placeholders in `docs/DEVPOST.md`.
- Submit before **August 10, 2026 at 5:00 PM EDT**, which is **August 11 at 2:30 AM IST**.
