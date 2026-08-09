"""Command-line entrypoint for web, CLI, and MCP modes."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .agent import RipplecheckAgent
from .mcp_server import serve_stdio
from .scenarios import SCENARIOS
from .transport import build_transport
from .web import run_web


ROOT = Path(__file__).resolve().parents[2]


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="ripplecheck",
        description="DataHub MCP counterfactual schema migration compiler",
    )
    commands = root.add_subparsers(dest="command")

    web = commands.add_parser("web", help="Run the deployable web demo")
    web.add_argument("--host", default="0.0.0.0")
    web.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))

    assess = commands.add_parser("assess", help="Assess one proposed schema change")
    assess.add_argument("change")
    assess.add_argument("--no-writeback", action="store_true")

    commands.add_parser("mcp", help="Run Ripplecheck as an MCP stdio server")
    commands.add_parser("scenarios", help="Print the built-in demo scenarios")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    command = args.command or "web"
    tools = build_transport(ROOT)
    try:
        if command == "web":
            host = getattr(args, "host", "0.0.0.0")
            port = getattr(args, "port", int(os.environ.get("PORT", "8000")))
            run_web(ROOT, tools, host, port)
        elif command == "assess":
            result = RipplecheckAgent(tools).assess(
                args.change, writeback=not args.no_writeback
            )
            print(json.dumps(result, indent=2))
        elif command == "mcp":
            serve_stdio(tools)
        elif command == "scenarios":
            print(json.dumps({"scenarios": SCENARIOS}, indent=2))
        return 0
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}")
        return 2
    finally:
        tools.close()
