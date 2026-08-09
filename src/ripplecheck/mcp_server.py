"""Expose Ripplecheck itself as a dependency-free MCP stdio server."""

from __future__ import annotations

import json
import sys
from typing import Any, TextIO

from .agent import RipplecheckAgent
from .scenarios import SCENARIOS
from .transport import DataHubTools


TOOLS = [
    {
        "name": "assess_schema_change",
        "description": (
            "Compile proposed DDL or a column change into a counterfactual DataHub graph, "
            "policy proof, release gate, migration DAG, and merge-ready evidence manifest."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "change": {
                    "type": "string",
                    "description": (
                        "Snowflake DDL or natural language, for example: ALTER TABLE "
                        "warehouse.analytics.customer_360 RENAME COLUMN customer_tier "
                        "TO loyalty_tier;"
                    ),
                },
                "writeback": {
                    "type": "boolean",
                    "default": True,
                    "description": "Append the hash-sealed decision capsule to the DataHub column.",
                },
            },
            "required": ["change"],
            "additionalProperties": False,
        },
    },
    {
        "name": "list_demo_scenarios",
        "description": "List the built-in offline scenarios and their expected decisions.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


class RipplecheckMCPServer:
    def __init__(self, tools: DataHubTools):
        self.agent = RipplecheckAgent(tools)

    def handle(self, message: dict[str, Any]) -> dict[str, Any] | None:
        method = message.get("method")
        request_id = message.get("id")
        if method == "notifications/initialized":
            return None
        if method == "initialize":
            return success(
                request_id,
                {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": "ripplecheck", "version": "2.0.0"},
                },
            )
        if method == "ping":
            return success(request_id, {})
        if method == "tools/list":
            return success(request_id, {"tools": TOOLS})
        if method == "tools/call":
            params = message.get("params", {})
            try:
                result = self._call_tool(params.get("name"), params.get("arguments", {}))
                return success(
                    request_id,
                    {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2, sort_keys=True),
                            }
                        ],
                        "structuredContent": result,
                        "isError": False,
                    },
                )
            except (ValueError, RuntimeError) as exc:
                return success(
                    request_id,
                    {
                        "content": [{"type": "text", "text": str(exc)}],
                        "isError": True,
                    },
                )
        if request_id is None:
            return None
        return error(request_id, -32601, f"Method not found: {method}")

    def _call_tool(self, name: str | None, arguments: dict[str, Any]) -> Any:
        if name == "assess_schema_change":
            return self.agent.assess(
                str(arguments.get("change", "")),
                writeback=bool(arguments.get("writeback", True)),
            )
        if name == "list_demo_scenarios":
            return {"scenarios": SCENARIOS}
        raise ValueError(f"Unknown tool: {name}")


def serve_stdio(
    tools: DataHubTools, input_stream: TextIO | None = None, output_stream: TextIO | None = None
) -> None:
    incoming = input_stream or sys.stdin
    outgoing = output_stream or sys.stdout
    server = RipplecheckMCPServer(tools)
    for line in incoming:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
            if not isinstance(message, dict):
                raise ValueError("MCP message must be a JSON object")
            response = server.handle(message)
        except (json.JSONDecodeError, ValueError) as exc:
            response = error(None, -32700, str(exc))
        if response is not None:
            outgoing.write(json.dumps(response, separators=(",", ":")) + "\n")
            outgoing.flush()


def success(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }
