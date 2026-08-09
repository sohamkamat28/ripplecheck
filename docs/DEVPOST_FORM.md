# Devpost form — exact copy/paste sheet

Use this page while completing the submission form. It reflects the live form fetched on August 10, 2026. Do not click the final **Submit** button until the video and personal attestations are complete.

## Project details

| Devpost field | Exact value |
| --- | --- |
| Project name | `Ripplecheck` |
| Tagline | `The DataHub MCP agent that compiles breaking warehouse DDL into a provable, owner-routed migration plan.` |
| Description | Paste all of [`DEVPOST.md`](DEVPOST.md), from **Short description** through **What's next**. Do not paste the final links/checklist notes. |
| Built with | `DataHub MCP Server`, `Model Context Protocol`, `Python 3.11`, `Snowflake DDL`, `dbt`, `Docker`, `GitHub Actions`, `HTML`, `CSS`, `JavaScript` |
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
| 27767 | Yes | DataHub technologies used | Select `DataHub MCP Server`. Select `DataHub OSS / Core Platform` only after a live local DataHub run has been completed and documented. Do not select ACK, Skills, or Analytics Agent. |
| 27768 | No | DataHub contribution | Leave blank. No upstream contribution is claimed. |
| 27840 | Yes | Country of residence | **ENTRANT MUST SELECT:** choose the actual country for every team member. Do not infer this from location or timezone. |
| 27841 | Yes | Newly created July 6–Aug 10? | Select `Yes, newly created during the Submission Period` only after personally confirming [`DISCLOSURES.md`](DISCLOSURES.md). |
| 27842 | No | Pre-existing code | `No pre-existing project code was incorporated. Standard Python tooling and an AI coding assistant (OpenAI Codex) were used; details and synthetic-data disclosure: https://github.com/sohamkamat28/ripplecheck/blob/main/docs/DISCLOSURES.md` |
| 27843 | Yes | Feedback Prize | Select `Yes, consider me for the Feedback Prize` only if submitting the complete, truthful feedback below. The live form exposes no “No” option. |

## Feedback Prize answers

These answers are written to be actionable without claiming a live setup that did not occur. Edit them if your personal experience differs.

### 27844 — What felt polished or useful?

The MCP tool split was useful for agent design: search resolves a catalog entity, schema fields verify the exact contract, lineage exposes downstream paths, batch entity lookup adds ownership and governance context, and description update provides a durable handoff. That sequence maps naturally to an evidence-first agent workflow. The challenge examples also made it clear that a strong agent should take bounded action and write knowledge back, rather than stop at a chat response.

### 27845 — Where did you get stuck or lose time?

The largest gap for an offline-first build was the distance between reading the MCP documentation and proving the same workflow against a small local DataHub instance. A single minimal guide that starts DataHub, ingests a tiny lineage-rich sample, launches the official MCP server, lists its exact tool names and argument shapes, and runs one JSON-RPC smoke test would remove a great deal of uncertainty. Clear version compatibility between DataHub OSS and the MCP package would also help.

### 27846 — What would you build or fix first?

I would ship a lightweight local “agent lab”: a small, version-pinned DataHub dataset with schema fields, column lineage, owners, criticality tags and an ML asset, plus automated MCP conformance tests. It matters because agent teams need to validate reads, writebacks, failure behavior and permission boundaries before they connect to production metadata. I would also add a structured decision-capsule aspect so agents can write machine-readable evidence without encoding it into prose descriptions.

### 27847 — Bugs or unexpected behavior

No reproducible DataHub product defect is claimed. The main issue was setup ambiguity: it was not obvious from one page which exact local versions, MCP launch command, tool schemas and writeback permissions formed the smallest supported end-to-end path. Expected: one copy-paste local smoke test. Observed: the pieces had to be assembled across multiple pages. A versioned quickstart with expected request and response examples would make failures much easier to distinguish from configuration errors.

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

