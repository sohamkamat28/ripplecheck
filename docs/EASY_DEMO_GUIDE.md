# Ripplecheck — easy side-by-side demo guide

**Open this demo:** [https://ripplecheck-datahub.vercel.app](https://ripplecheck-datahub.vercel.app)
**Target video length:** 2 minutes 40 seconds  
**Challenge category:** Agents That Do Real Work  
**Cost:** $0 — the complete recording path works offline without an API key.

Keep this guide beside the browser. Read the **SAY** column while doing only the action in the **CLICK / SHOW** column. Speak slowly; you do not need to memorize anything.

## Before you press Record

1. Confirm [https://ripplecheck-datahub.vercel.app](https://ripplecheck-datahub.vercel.app) opens and says **Offline graph ready**.
2. Set browser zoom to **80%** and close unrelated tabs and notifications.
3. Refresh the page. Leave the default DDL and checked writeback option unchanged.
4. Put this guide on one side of the screen and the demo browser on the other.
5. Start recording with the large headline visible.

## One-take script

| Time | CLICK / SHOW — what your hand does | SAY — read this aloud |
| --- | --- | --- |
| **0:00–0:18** | Show the headline **Compile the change before it compiles you.** Do not click. | “A simple warehouse rename can silently break data pipelines, machine-learning features, and executive dashboards. Ripplecheck uses DataHub metadata to catch that damage and build the fix before the change reaches production.” |
| **0:18–0:36** | Scroll to **Proposed DDL**. Point at `customer_tier` and `loyalty_tier`. | “Here I am renaming `customer_tier` to `loyalty_tier` on our canonical customer table. The demo is completely offline and free, while preserving the same DataHub MCP tool contract used in live mode.” |
| **0:36–0:55** | Click the orange **Compile migration plan** button once. Wait until **Release gate CLOSED** appears. | “I will compile the migration, not execute it. The agent resolves the field, traverses column lineage, checks owners and criticality, applies release policy, and seals the result as an auditable decision capsule.” |
| **0:55–1:18** | Stay on **Counterfactual**. Point to **10/10 risk**, **5 broken edges**, and **80% owner coverage**. | “The direct rename is blocked at ten out of ten risk. The counterfactual graph finds five broken dependencies across Airflow, dbt, a production churn model, and two dashboards. It also exposes an ownership gap instead of hiding it.” |
| **1:18–1:39** | Click **Policy proof**. Point briefly at the red failed rules. | “The decision is deterministic and explainable. Stable rule IDs prove that active consumers, critical assets, the production model, and reversibility are not yet safe. The release gate opens only when every failed condition is fixed.” |
| **1:39–2:02** | Click **Execution DAG**. Move the cursor from the first gate downward through the steps. | “Ripplecheck does more than report impact. It compiles an owner-routed execution plan: freeze the unsafe DDL, add the new field, publish a dual-read compatibility layer, migrate each consumer, prove parity, and require human approval before retiring the old field.” |
| **2:02–2:22** | Click **MCP trace**. Point down the five calls. | “Every metadata action is inspectable. The trace shows DataHub MCP search, schema inspection, lineage traversal, entity enrichment, and the hash-sealed writeback—with exact arguments and no opaque risk score.” |
| **2:22–2:40** | Scroll slightly to **Merge-ready evidence pack**. Point at the six files, then click **Download PR pack (.zip)**. | “Finally, the agent ships the handoff: compatibility SQL, a dbt contract patch, parity tests, owner routing, the review decision, and a tamper-evident capsule. Ripplecheck turns DataHub into an active release gate, and the full Apache 2.0 demo runs with one command.” |

**Stop recording as soon as the ZIP download starts.**

## Your five-click memory aid

If you lose your place, remember this sequence:

1. **Compile migration plan**
2. **Policy proof**
3. **Execution DAG**
4. **MCP trace**
5. **Download PR pack (.zip)**

## Numbers worth emphasizing

| What judges see | Expected result |
| --- | --- |
| Decision | **BLOCK** |
| Release gate | **CLOSED** |
| Risk | **10/10** |
| Broken dependencies | **5** |
| Critical consumers | **3** |
| Owner coverage | **80%** |
| DataHub MCP calls | **5** |
| Generated PR files | **6** |

## Tech stack: why each part matters

| Technology | Why it is used | What it delivers in the demo |
| --- | --- | --- |
| **DataHub MCP contract** | Makes DataHub's schema, lineage, ownership, tags, and descriptions available as tools | Five visible, auditable metadata calls instead of invented context |
| **Offline DataHub graph fixture** | Removes credentials, paid billing, networking, and judge setup risk | A deterministic zero-cost demo with realistic cross-system lineage |
| **Python 3.11 standard library** | Keeps the agent portable and installation-free | DDL parsing, graph traversal, policy evaluation, API serving, and writeback |
| **Counterfactual graph engine** | Projects the proposed after-state without changing production | Exact broken edges, failure paths, lineage depth, and ownership coverage |
| **Stable policy rules** | Makes release decisions reproducible and CI-friendly | Explainable `PASS`, `WARN`, and `FAIL` evidence with stable rule IDs |
| **Owner-routed execution DAG** | Converts impact analysis into sequenced work | A zero-downtime migration plan with actors, prerequisites, and approval gates |
| **Canonical JSON + SHA-256** | Makes evidence portable and tamper-evident | A hash-sealed decision capsule that can be verified later |
| **HTML, CSS, and vanilla JavaScript** | Avoids a build step and loads instantly | The responsive evidence console used in the recording |
| **ZIP evidence compiler** | Packages the result for the normal pull-request workflow | Six downloadable, merge-ready migration artifacts |

## If something goes wrong on camera

- **Nothing appears after Compile:** wait two seconds. If still blank, stop recording, refresh, and restart the take.
- **Wrong scenario is loaded:** click **Rename a production contract**, then compile again.
- **You forget the narration:** describe only what is visible, then move to the next tab. The five-click sequence keeps the story intact.
- **Download is blocked:** point at the six files and say the final sentence. Do not troubleshoot during the recording.
- **The hosted page does not open:** use the local fallback [http://127.0.0.1:8765](http://127.0.0.1:8765). Keep the local server running during the recording.

## Optional judge answer

If asked, “Where is the AI?” say:

> “The agent autonomously gathers DataHub evidence, projects impact, evaluates policy, assigns remediation work, writes back provenance, and compiles the PR pack. The final gate is deliberately deterministic because production governance must be reproducible and auditable. A language model can extend parsing or suggestions without receiving authority over the release decision.”
