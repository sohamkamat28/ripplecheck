# Official-rules compliance matrix

Source: [Build with DataHub: The Agent Hackathon Official Rules](https://datahub.devpost.com/rules), reviewed August 10, 2026. The official rules control if this checklist differs from them.

## 1. Dates and submission lock

| Requirement | Ripplecheck evidence or action |
| --- | --- |
| Submit between July 6, 2026 at 9:00 AM EDT and August 10, 2026 at 5:00 PM EDT | Submit no later than August 11 at 2:30 AM IST; internal target is August 10 at 10:30 PM IST. |
| Feedback submission uses the same closing time | Optional; complete at most one actionable feedback survey before the deadline. |
| Judging runs August 17 through August 31, 2026 | Keep the repository and demo free, public, and unchanged in accessibility through August 31 at 5:00 PM EDT. |
| No substantive submission edits after the deadline | Freeze and verify every submitted URL before final submission. Post-deadline changes are allowed only when specifically permitted for inappropriate, infringing, or personally identifying material. |

## 2. Entrant eligibility — manual attestations

The entrant must personally confirm each item; code cannot prove these facts.

- [ ] I am at least the legal age of majority where I live.
- [ ] I am not resident in an excluded jurisdiction and local or U.S. law does not prohibit participation or receipt of a prize.
- [ ] I am not a hackathon judge; employed by a judge; involved in organizing, administering, promoting, or judging the hackathon; an employee, representative, agent, parent, subsidiary, affiliate, or disallowed family/household member of a promotion entity; or otherwise subject to a conflict of interest.
- [ ] If submitting as a team or organization, all members are eligible and I am the authorized representative.
- [ ] I have joined the hackathon through Devpost and will complete every required submission-form field before the deadline.

## 3. Project requirements

| Requirement | Evidence | Status |
| --- | --- | --- |
| Working software application | Web app, CLI, JSON API, and MCP server; automated tests and health endpoint | Ready |
| Uses DataHub open source plus MCP Server, Agent Context Kit, DataHub Skills, or Analytics Agent | Official DataHub MCP stdio transport exists; fixture preserves tool semantics | **Live end-to-end DataHub proof still recommended before submission** |
| Fits a challenge | Primary: Agents That Do Real Work; also strongly aligns with Metadata-Aware Code Generation | Ready |
| Reads context, acts, and writes back | Schema, lineage, owners, tags, policy, generated code, execution DAG, and `update_description` capsule | Ready in fixture; live transport available |
| Runs consistently as depicted and described | Dependency-free fixture path, Docker, Render Blueprint, tests, preflight | Ready |
| Built during submission period | See `docs/DISCLOSURES.md` | Entrant attestation required |
| Disclose pre-existing code | No pre-existing project code declared; AI coding assistance disclosed | Ready |
| Authorized third-party SDK/API/data use | Standard library default; official Apache-2.0 MCP server optional; synthetic data | Ready |

## 4. Mandatory submission materials

| Material | Requirement | Ripplecheck status |
| --- | --- | --- |
| Project URL | Free, unrestricted website, functioning demo, or test build | Public URL pending |
| Public source repository | Full source, assets, and instructions | GitHub URL pending |
| Apache 2.0 | Root license detected and visible on repository page | Root `LICENSE` ready; verify after push |
| Text description | Features, functionality, technology, and data | `docs/DEVPOST.md` ready |
| Demonstration video | Under 3 minutes, working software shown, public on YouTube/Vimeo/Youku, link included | User preparing |
| Video rights | No unlicensed music, third-party footage, marks, or other copyrighted material | Record only Ripplecheck; crop unrelated browser/desktop content; use no music |
| Sample outputs | Recommended generated code/reports/transforms | JSON in `samples/`; extracted artifacts in `examples/` |
| English | All materials in English or translated | Ready |

## 5. Testing and availability

- The project must be testable free of charge and without restriction through the end of judging.
- A private site would require working judge credentials; Ripplecheck instead provides a public, no-login path.
- Judges may judge only from the description, screenshots, and video, so those materials must independently explain the problem, DataHub usage, action, writeback, and outputs.
- The project uses ordinary desktop hardware and requires no proprietary device.
- Exact judge steps and expected results are in `docs/TESTING.md`.

## 6. Ownership, licenses, privacy, and security

- [ ] Entrant confirms the submission is original, solely owned by the entrant/team, and does not violate copyright, trademark, patent, contract, privacy, publicity, or other rights.
- Open-source dependencies must be used under their licenses and Ripplecheck must add new functionality; see `NOTICE` and `docs/DISCLOSURES.md`.
- No trade secrets, private customer data, personal email addresses, credentials, or proprietary datasets are included.
- The repository secret scan must remain clean; `.env` and local writeback state are gitignored.
- Submitted content must contain no virus, spyware, malicious code, or disabling device.
- The project must not have received prohibited financial or preferential support from DataHub or Devpost; entrant must confirm.

## 7. Multiple entries and representation

- Multiple submissions are allowed only when each is unique and substantially different.
- A team or organization must appoint an eligible representative, who receives and allocates any prize.
- Each eligible submission may win only one project prize. An individual may separately receive at most one feedback prize.

## 8. Judging alignment

Stage One is pass/fail for theme fit and reasonable application of the required APIs/SDKs. Stage Two criteria are equally weighted:

| Criterion | Ripplecheck proof |
| --- | --- |
| Use of DataHub | Five-tool evidence loop across schema, lineage, ownership, governance, and writeback |
| Technical execution | End-to-end web/CLI/MCP paths, deterministic policies and artifacts, tests, CI, Docker, deploy config |
| Originality | Counterfactual migration compiler rather than catalog chat or a flat blast-radius list |
| Real-world usefulness | Prevents schema breakage, assigns remediation, and produces review-ready code |
| Submission quality | One-command judge path, screenshot, samples, exact testing guide, prepared Devpost copy and video script |
| Optional open-source bonus | No upstream DataHub contribution currently claimed |

Use of DataHub is the first tie-breaker, followed by the remaining criteria in listed order.

## 9. Submission and proof of receipt

- Save a draft early, but complete and submit it before the deadline.
- After submission, open the project from **My projects**, verify every link, and save a screenshot or PDF of the confirmation.
- Proof of sending is not proof of receipt; if the entry is lost or corrupted, request resubmission promptly.

## 10. Legal terms acknowledged by submission

Submission accepts the official rules as a contract and the binding decisions of Sponsor, Administrator, and judges. The entrant retains ownership but grants the Sponsor a non-exclusive judging license and permits hackathon publicity using submitted work and contributors' name, likeness, voice, image, comments, hometown, and country for the stated period. Prize recipients must pass identity, qualification, and contribution verification; return required forms within ten business days; and handle applicable fees, banking rules, currency conversion, withholding, and taxes. The rules also contain releases, liability limitations, arbitration/class-action waiver terms where enforceable, New York governing law, publicity consent, Devpost Terms of Service incorporation, and privacy-policy terms. Review the official rules personally before clicking Submit.

## Final manual fields

- [ ] Entrant or team member names
- [ ] Eligibility and conflict attestations
- [ ] Primary challenge category
- [ ] Public project URL
- [ ] Public GitHub URL
- [ ] Public video URL under 3 minutes
- [ ] Cover image
- [ ] Project description
- [ ] Technologies used: DataHub MCP Server; DataHub OSS/Core Platform only if actually demonstrated
- [ ] Optional feedback survey
- [ ] Final receipt screenshot/PDF
