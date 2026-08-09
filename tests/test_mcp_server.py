from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ripplecheck.mcp_server import RipplecheckMCPServer
from ripplecheck.transport import FixtureDataHubTools


class MCPServerTests(unittest.TestCase):
    def setUp(self) -> None:
        tools = FixtureDataHubTools(ROOT / "data" / "catalog.json")
        self.server = RipplecheckMCPServer(tools)

    def test_initializes_and_lists_tools(self) -> None:
        initialized = self.server.handle(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        )
        self.assertEqual(initialized["result"]["serverInfo"]["name"], "ripplecheck")
        listed = self.server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        self.assertEqual(
            [tool["name"] for tool in listed["result"]["tools"]],
            ["assess_schema_change", "list_demo_scenarios"],
        )

    def test_tool_call_returns_structured_result(self) -> None:
        response = self.server.handle(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "assess_schema_change",
                    "arguments": {
                        "change": "Drop column legacy_bucket from warehouse.sandbox.experiment_flags",
                        "writeback": False,
                    },
                },
            }
        )
        self.assertFalse(response["result"]["isError"])
        self.assertEqual(response["result"]["structuredContent"]["decision"], "SAFE")


if __name__ == "__main__":
    unittest.main()

