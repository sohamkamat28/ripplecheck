# Project disclosures

## Creation period

Ripplecheck was created for **Build with DataHub: The Agent Hackathon** during the official submission period, July 6 through August 10, 2026. No pre-existing proprietary project or commercially funded version of Ripplecheck was incorporated.

## Development assistance

OpenAI Codex was used as a permitted AI coding assistant for implementation, testing, documentation, and interface iteration. The entrant directed the project, selected the problem and architecture, reviewed the output, and owns the submitted work.

## Open-source and third-party technology

- Ripplecheck source code is released under Apache License 2.0.
- The optional official DataHub MCP Server is an external Apache-2.0 project and is not vendored into this repository.
- The offline judge path uses only the Python standard library and contains no third-party runtime package.
- DataHub names and MCP tool names are used only to describe interoperability. DataHub is a trademark of its respective owner; no endorsement is implied.
- The application screenshot and interface assets in this repository were created from Ripplecheck itself. No third-party photographs, music, logos, templates, or proprietary datasets are included.

## Data

`data/catalog.json` is a synthetic retail metadata graph created for the hackathon. Entity names, owners, email addresses, fields, tags, and lineage are fictional. Email addresses use the reserved `.example` domain. Fixture mode does not claim to be a live DataHub Cloud connection.

## Safety and scope

- Submitted DDL is parsed but never executed.
- Generated SQL, YAML, tests, and routing files are review artifacts and are never applied automatically.
- Fixture writeback is stored locally in the gitignored `data/run-state.json` file.
- Live mode connects to the official DataHub MCP Server and never silently falls back to fixture data.
