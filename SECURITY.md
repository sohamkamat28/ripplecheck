# Security policy

## Supported period

The public hackathon build is supported for judge testing through August 31, 2026 at 5:00 PM EDT.

## Reporting

Please report a suspected vulnerability privately through GitHub's **Report a vulnerability** feature rather than opening a public issue with exploit details.

## Safety model

- Ripplecheck never executes submitted DDL.
- Generated SQL, YAML, tests, and routing are review artifacts only.
- Fixture mode needs no secret and stores local writeback state in a gitignored file.
- Live DataHub credentials are supplied only to the external official MCP server through its supported configuration; they are not committed to this repository.
- The HTTP demo rejects oversized request bodies and prevents static path traversal.
