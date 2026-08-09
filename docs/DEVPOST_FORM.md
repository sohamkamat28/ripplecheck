# Devpost form — exact copy/paste sheet

Use this page while completing the submission form. It reflects the live form fetched on August 10, 2026. Do not click the final **Submit** button until the video and personal attestations are complete.

## Project details

| Devpost field | Exact value |
| --- | --- |
| Project name | `Ripplecheck` |
| Tagline | `The DataHub MCP agent that compiles breaking warehouse DDL into a provable, owner-routed migration plan.` |
| Description | Paste all of [`DEVPOST.md`](DEVPOST.md), from **Short description** through **What's next**. Do not paste the final links/checklist notes. |
| Built with | `DataHub OSS / Core Platform`, `DataHub MCP Server`, `Model Context Protocol`, `Python 3.11`, `Snowflake DDL`, `dbt`, `Docker`, `GitHub Actions`, `HTML`, `CSS`, `JavaScript` |
| Public repository | `https://github.com/sohamkamat28/ripplecheck` |
| Project URL | `https://github.com/sohamkamat28/ripplecheck` — the host explicitly permits a repository with clear setup instructions; replace only if a public deployment is verified |
| Sample outputs | `https://github.com/sohamkamat28/ripplecheck/tree/main/examples` |
| Video | **PENDING:** paste the public YouTube or Vimeo URL; verify in an incognito window and keep runtime below 3:00 |
| Cover image | Upload `docs/ripplecheck-result.png` |

## Hackathon-specific fields

| ID | Required | Question | Answer |
| --- | --- | --- | --- |
| 27765 | Yes | Which challenge category? | `Agents That Do Real Work` |
| 27838 | Yes | Public code repository | `https://github.com/sohamkamat28/ripplecheck` |
| 27837 | No | Easy-access Project URL | `https://github.com/sohamkamat28/ripplecheck` unless a verified public deployment is available |
| 27839 | No | Generated-artifact examples | `https://github.com/sohamkamat28/ripplecheck/tree/main/examples` |
| 27767 | Yes | DataHub technologies used | Select both `DataHub OSS / Core Platform` and `DataHub MCP Server`. Both completed a documented live read/write run. Do not select ACK, Skills, or Analytics Agent. |
| 27768 | No | DataHub contribution | Leave blank. No upstream contribution is claimed. |
| 27840 | Yes | Country of residence | **ENTRANT MUST SELECT:** choose the actual country for every team member. Do not infer this from location or timezone. |
| 27841 | Yes | Newly created July 6–Aug 10? | Select `Yes, newly created during the Submission Period` only after personally confirming [`DISCLOSURES.md`](DISCLOSURES.md). |
| 27842 | No | Pre-existing code | `No pre-existing project code was incorporated. Standard Python tooling and an AI coding assistant (OpenAI Codex) were used; details and synthetic-data disclosure: https://github.com/sohamkamat28/ripplecheck/blob/main/docs/DISCLOSURES.md` |
| 27843 | Yes | Feedback Prize | Select `Yes, consider me for the Feedback Prize` only if submitting the complete, truthful feedback below. The live form exposes no “No” option. |

## Feedback Prize answers

These answers reflect the completed local DataHub OSS + official MCP setup and are written to be specific and actionable. Edit them only if your personal experience differs.

### 27844 — What felt polished or useful?

The MCP tool split was useful for agent design: search resolved a catalog entity, schema fields verified the exact contract, lineage exposed downstream paths, batch entity lookup added ownership and governance context, and description update provided a durable handoff. In the live test, that sequence let Ripplecheck find 23 downstream assets and successfully append its result to the source column. It maps naturally to an evidence-first agent workflow instead of stopping at a chat response.

### 27845 — Where did you get stuck or lose time?

The largest time cost was assembling the smallest supported local path across separate pages: DataHub OSS Quickstart, sample ingestion, personal access tokens, the current `uvx mcp-server-datahub@latest` command, mutation opt-in, and the exact response envelopes. A single version-pinned guide that starts DataHub, loads `showcase-ecommerce`, creates or explains the token, launches MCP, and runs one read plus one write smoke test would remove uncertainty. Expected payload examples would also make transport integration faster.

### 27846 — What would you build or fix first?

I would ship a lightweight local “agent lab”: a small, version-pinned DataHub dataset with schema fields, column lineage, owners, criticality tags and an ML asset, plus automated MCP conformance tests. It matters because agent teams need to validate reads, writebacks, failure behavior and permission boundaries before they connect to production metadata. I would also add a structured decision-capsule aspect so agents can write machine-readable evidence without encoding it into prose descriptions.

### 27847 — Bugs or unexpected behavior

On a fresh DataHub OSS 1.6.0 Docker Quickstart, `datahub init --username datahub --password datahub` failed with `'NoneType' object has no attribute 'get'`. The GMS log showed the default `datahub` user was unauthorized to create a personal access token, while the generated quickstart environment had metadata-service authentication disabled. Expected: initialization should either create the token, clearly explain that no token is needed in auth-disabled local mode, or report the permission problem directly. Observed: the CLI surfaced an unrelated `NoneType` error. The MCP run itself worked after supplying the required token variable with a non-secret placeholder in this auth-disabled local instance.

## Personal confirmations before final submission

- [ ] I meet the age and geographic eligibility rules.
- [ ] I have no disqualifying role, relationship, support, or conflict of interest.
- [ ] I am the entrant or authorized team representative.
- [ ] Every team member and country is correctly listed.
- [ ] The project was newly created during the submission period and the disclosure is accurate.
- [ ] I own or am authorized to use every submitted component and visual.
- [ ] The video is public, under three minutes, shows the working product, and contains no unlicensed music, marks, or footage.
- [ ] Every submitted URL works in an incognito window without login or payment.
- [ ] The final preview is correct, the entry is submitted before August 11, 2026 at 2:30 AM IST, and proof of receipt is saved.
