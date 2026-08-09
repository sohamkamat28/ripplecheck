# Ripplecheck — final one-flow demo pitch

**Demo:** [https://ripplecheck-datahub.vercel.app](https://ripplecheck-datahub.vercel.app)
**Target:** about 2 minutes 45 seconds  
**Category:** Agents That Do Real Work

This version is one continuous conversation. Speak only the normal paragraphs. The short italic lines are silent screen directions.

## Set up before recording

1. Open the demo, refresh it, and set browser zoom to 80%.
2. Confirm **Offline graph ready** is visible.
3. Leave the default rename unchanged and keep writeback checked.
4. Copy this second input now so it is ready to paste near the end:

```sql
ALTER TABLE warehouse.sandbox.experiment_flags ALTER COLUMN legacy_bucket SET DATA TYPE VARCHAR(64);
```

## Read this from beginning to end

*Start with the main headline visible. Look at the camera for the first sentence, then look toward the demo.*

Hi, I’m Soham, and this is Ripplecheck. Built for agents that do real work. One warehouse rename can break pipelines, ML models, and dashboards. DataHub knows these connections, and Ripplecheck checks the impact before the change reaches production.

*Scroll to the Proposed DDL and point at the old and new column names.*

Here I’m renaming `customer_tier` to `loyalty_tier` on our main customer table. Let’s see what happens if I merge it.

*Click **Compile migration plan**. Wait for **Release gate CLOSED**.*

Compile does not run the DDL. It uses DataHub MCP to check the column, follow its lineage, find the owners, apply release rules, and save the decision for whoever comes next.

*Stay on Counterfactual. Point at **10/10**, **5 broken edges**, and **80% owner coverage**.*

Here’s the result. The rename is blocked at ten out of ten risk. Ripplecheck found five affected assets: Airflow, dbt, a production ML model, and two dashboards. It shows each impact path and one missing owner.

*Click **Policy proof** and point at the failed rules.*

The policy proof explains why. Each result has a rule and evidence, not a mystery score. Consumers have not moved, the model is unprotected, and there is no rollback. It states what will open the gate.

*Click **Execution DAG** and move the pointer slowly down the plan.*

Then Ripplecheck builds the fix: add the new field, keep the old one working, route tasks to their owners, compare both versions, and require approval before cleanup. The team gets an ordered, zero-downtime plan.

*Click **MCP trace** and point down the calls.*

The MCP trace shows search, schema, lineage, owners, and writeback. This demo uses an offline DataHub snapshot; connect the official MCP server and the same workflow runs live.

*Scroll to the evidence pack. Point to each file group while explaining it. Then click **Download PR pack (.zip)**. You do not need to open Finder; the paths shown here are the exact paths inside the downloaded ZIP.*

Inside the download, `migration` has the compatibility SQL, `models` has the dbt contract, and `tests` has the parity check. `review` contains the decision and owner routing, while `manifest` holds the signed evidence capsule: six real files, ready for a pull request.

*Scroll back to Proposed DDL, but do not paste yet.*

Now I’ll try a query that is not a preset. It changes the deprecated `legacy_bucket` field in a development table to `VARCHAR(64)`. DataHub shows nothing depends on it, so a real graph evaluation should call it safe.

*Select all text in Proposed DDL, paste the second input, and click **Compile migration plan**. Wait for **Release gate OPEN**, then point at **0/10** and **0 broken edges**.*

And it does: zero risk, no broken edges, and an open release gate. It is the same agent and rules, but a different input produces a different decision.

*Keep the open gate visible. Stop moving the pointer and finish calmly.*

That’s Ripplecheck: an active DataHub release gate that catches impact before production. It is Apache 2.0 open source and runs with one command. Thank you.

## Simple click order if you lose your place

**Compile → Policy proof → Execution DAG → MCP trace → Download → Paste second input → Compile**

Do not try to sound memorized. Imagine one judge asked, “What does Ripplecheck do?” and you are simply showing them the answer.
