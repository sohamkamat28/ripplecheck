from pathlib import Path
from io import BytesIO
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ripplecheck.agent import RipplecheckAgent
from ripplecheck.evidence_pack import build_evidence_pack
from ripplecheck.parser import parse_change_request
from ripplecheck.transport import FixtureDataHubTools


class ParserTests(unittest.TestCase):
    def test_parses_drop(self) -> None:
        request = parse_change_request(
            "Drop column customer_tier from warehouse.analytics.customer_360"
        )
        self.assertEqual(request.action, "drop")
        self.assertEqual(request.column, "customer_tier")

    def test_parses_rename(self) -> None:
        request = parse_change_request(
            "Rename column net_revenue to recognized_revenue in warehouse.finance.monthly_revenue"
        )
        self.assertEqual(request.action, "rename")
        self.assertEqual(request.replacement, "recognized_revenue")

    def test_parses_snowflake_rename_ddl(self) -> None:
        request = parse_change_request(
            "ALTER TABLE warehouse.analytics.customer_360 "
            "RENAME COLUMN customer_tier TO loyalty_tier;"
        )
        self.assertEqual(request.action, "rename")
        self.assertEqual(request.dataset, "warehouse.analytics.customer_360")
        self.assertEqual(request.replacement, "loyalty_tier")

    def test_parses_snowflake_drop_and_type_ddl(self) -> None:
        dropped = parse_change_request(
            "ALTER TABLE warehouse.sandbox.experiment_flags DROP COLUMN legacy_bucket;"
        )
        changed = parse_change_request(
            "ALTER TABLE warehouse.analytics.customer_360 "
            "ALTER COLUMN lifetime_value SET DATA TYPE NUMBER(20, 4);"
        )
        self.assertEqual(dropped.action, "drop")
        self.assertEqual(changed.action, "type_change")
        self.assertEqual(changed.target_type, "NUMBER(20, 4)")


class AgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tools = FixtureDataHubTools(ROOT / "data" / "catalog.json")
        self.agent = RipplecheckAgent(self.tools)

    def test_blocks_customer_tier_drop_and_writes_back(self) -> None:
        result = self.agent.assess(
            "Drop column customer_tier from warehouse.analytics.customer_360"
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(len(result["blast_radius"]), 5)
        self.assertEqual(result["risk_score"], 10)
        self.assertTrue(result["writeback"]["success"])
        self.assertEqual(
            [call["tool"] for call in result["tool_trace"]],
            ["search", "list_schema_fields", "get_lineage", "get_entities", "update_description"],
        )

    def test_allows_unconsumed_sandbox_drop(self) -> None:
        result = self.agent.assess(
            "Drop column legacy_bucket from warehouse.sandbox.experiment_flags"
        )
        self.assertEqual(result["decision"], "SAFE")
        self.assertEqual(result["blast_radius"], [])
        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["release_gate"]["status"], "OPEN")
        self.assertEqual(result["release_gate"]["blockers"], [])
        self.assertIn(
            "models/experiment_flags/schema.yml",
            [item["path"] for item in result["artifact_manifest"]],
        )

    def test_rejects_missing_column(self) -> None:
        with self.assertRaisesRegex(ValueError, "was not found"):
            self.agent.assess(
                "Drop column imaginary_field from warehouse.analytics.customer_360"
            )

    def test_fixture_writeback_survives_a_new_transport(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "run-state.json"
            tools = FixtureDataHubTools(ROOT / "data" / "catalog.json", state_path)
            result = RipplecheckAgent(tools).assess(
                "Drop column customer_tier from warehouse.analytics.customer_360"
            )
            self.assertTrue(state_path.is_file())

            reloaded = FixtureDataHubTools(ROOT / "data" / "catalog.json", state_path)
            schema = reloaded.call_tool(
                "list_schema_fields",
                {"urn": result["source"]["urn"], "keywords": ["customer_tier"]},
            )
            self.assertIn("Ripplecheck decision", schema["fields"][0]["description"])

    def test_compiles_counterfactual_policy_and_dag(self) -> None:
        result = self.agent.assess(
            "ALTER TABLE warehouse.analytics.customer_360 "
            "RENAME COLUMN customer_tier TO loyalty_tier;",
            writeback=False,
        )
        self.assertEqual(result["release_gate"]["status"], "CLOSED")
        self.assertEqual(result["counterfactual"]["metrics"]["broken_edges"], 5)
        self.assertEqual(result["counterfactual"]["metrics"]["ownership_coverage"], 80)
        self.assertEqual(result["blast_radius"][-1]["lineage_path"][-1], "tableau.retention_operations")
        self.assertIn("RC-021", result["release_gate"]["blockers"])
        self.assertEqual(result["execution_plan"][-1]["id"], "G1")

    def test_evidence_pack_is_deterministic_and_complete(self) -> None:
        result = self.agent.assess(
            "ALTER TABLE warehouse.analytics.customer_360 "
            "RENAME COLUMN customer_tier TO loyalty_tier;",
            writeback=False,
        )
        first = build_evidence_pack(result)
        second = build_evidence_pack(result)
        self.assertEqual(first, second)
        with ZipFile(BytesIO(first)) as archive:
            self.assertEqual(
                sorted(archive.namelist()),
                sorted(item["path"] for item in result["artifact_manifest"]),
            )
            sql = archive.read("migration/compatibility_view.sql").decode("utf-8")
            self.assertIn("ADD COLUMN IF NOT EXISTS loyalty_tier STRING", sql)
            capsule = archive.read("manifest/change-capsule.json").decode("utf-8")
            self.assertIn(result["change_capsule"]["capsule_id"], capsule)


if __name__ == "__main__":
    unittest.main()
