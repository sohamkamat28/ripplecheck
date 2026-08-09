# Judge testing instructions

Ripplecheck is free to test and requires no login, API key, paid model, warehouse, or network connection for the default path.

## Requirements

- Python 3.11 or newer
- A desktop browser

## One-command test

```bash
python3 main.py web --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`, keep the default DDL, and click **Compile migration plan**.

Expected result:

- decision `BLOCK`;
- release gate `CLOSED`;
- risk `10/10`;
- 5 affected assets and 80% owner coverage;
- 5 DataHub MCP-contract calls including writeback;
- 6 downloadable pull-request files.

If port 8000 is occupied, use another port, for example:

```bash
python3 main.py web --host 127.0.0.1 --port 8765
```

## Dynamic result check

Replace the input with:

```sql
ALTER TABLE warehouse.sandbox.experiment_flags
ALTER COLUMN legacy_bucket SET DATA TYPE VARCHAR(64);
```

Compile again. Expected result: `SAFE`, release gate `OPEN`, risk `0/10`, and zero broken edges. This request is not a listed preset.

## Automated verification

```bash
make samples
make verify
```

The test suite covers parsing, graph traversal, policy decisions, execution gates, writeback persistence, MCP protocol behavior, deterministic ZIP bytes, generated file names and content, and packaging checks.

## Inspect outputs without running

- Full assessment JSON is checked into `samples/`.
- Extracted generated SQL, YAML, Markdown, and JSON files are checked into `examples/`.
- `docs/ripplecheck-result.png` shows the compiled default result.

## Optional live DataHub mode

After initializing the official DataHub MCP Server against a DataHub OSS or Cloud instance:

```bash
export RIPPLECHECK_MODE=live
export DATAHUB_MCP_COMMAND="npx -y @acryldata/mcp-server-datahub"
export TOOLS_IS_MUTATION_ENABLED=true
python3 main.py web --host 127.0.0.1 --port 8000
```

Mutation tools are opt-in. Unset `TOOLS_IS_MUTATION_ENABLED` and disable the writeback checkbox for a read-only live assessment. Live connection errors are returned to the user and never fall back silently to the fixture.

## Availability

The public repository and hosted judge path must remain public, free and unrestricted through the end of judging on August 31, 2026 at 5:00 PM EDT.
