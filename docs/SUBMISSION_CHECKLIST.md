# Aug 10 shipping checklist

The exhaustive rule-by-rule audit is in [RULES_COMPLIANCE.md](RULES_COMPLIANCE.md). Eligibility, conflicts, ownership, project dates, team representation, and prize/tax declarations require the entrant's personal confirmation.

Official deadline: **Monday, August 10, 2026 at 5:00 PM EDT**

India equivalent: **Tuesday, August 11, 2026 at 2:30 AM IST**

Internal target: **August 10 at 10:30 PM IST**, four hours before the deadline.

## Ship in this order

### Code freeze: by Aug 9, 8:00 PM IST

- Run `make samples && make verify`.
- Start `python3 main.py web` and run all three scenarios.
- Confirm `/health` returns HTTP 200.
- Check the page at desktop and mobile widths.
- Stop feature work after this point unless the core demo is broken.

### Publish: by Aug 9, 10:00 PM IST

- [x] Create public repository: `https://github.com/sohamkamat28/ripplecheck`.
- [x] Push the default branch.
- [x] Confirm GitHub Actions is green.
- [x] Verify anonymous repository, README, license, and sample access.
- [x] Confirm the root license is detected as Apache-2.0.
- [x] Confirm `docs/DISCLOSURES.md`, `docs/TESTING.md`, and `examples/` are public.

### Deploy: by Aug 10, 12:00 PM IST

- The official submission instructions allow the public repository with clear setup instructions to serve as the Project URL; this path is ready and requires no paid account.
- If a Render account is already available, optionally create the included Blueprint, wait for `/health`, and test both default and safe scenarios.
- Do not substitute an unverified or short-lived tunnel for the durable repository URL.
- Keep the local demo ready as a recording fallback.

### Record: by Aug 10, 5:00 PM IST

- Follow `docs/DEMO_RUNBOOK.md` exactly.
- Keep the final cut below 3 minutes.
- Upload at 1080p with captions.
- Use public or unlisted visibility.
- Verify playback in an incognito window.

### Submit: by Aug 10, 10:30 PM IST

- Choose **Agents That Do Real Work**.
- Use `docs/DEVPOST_FORM.md` for exact field-by-field answers and `docs/DEVPOST.md` for the writeup.
- Add the public repo, live demo, and video URLs.
- Use the compiled-result screenshot as the cover image.
- Preview every section and follow every external link.
- Submit once, then verify the project appears under **My projects**.
- Save a PDF or screenshot of the confirmation page.
- Keep the repository and demo free and publicly accessible through August 31, 2026 at 5:00 PM EDT.
- Do not make substantive submission changes after the deadline.

## Only if time remains

- Complete the hackathon feedback survey for the feedback prize.
- Add a short GIF to the README.
- Open a DataHub Skills Registry contribution or documentation PR.

Do not trade submission certainty for a late feature. A working URL, clear video, exact DataHub trace, and honest README score across every judging criterion.
