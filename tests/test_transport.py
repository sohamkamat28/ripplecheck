from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ripplecheck.transport import normalize_official_result


class OfficialResponseNormalizationTests(unittest.TestCase):
    def test_normalizes_search_entity_properties(self) -> None:
        result = normalize_official_result(
            "search",
            {
                "searchResults": [
                    {
                        "entity": {
                            "urn": "urn:li:dataset:(urn:li:dataPlatform:dbt,orders,PROD)",
                            "properties": {"name": "orders"},
                            "platform": {"name": "dbt"},
                        }
                    }
                ]
            },
        )

        entity = result["searchResults"][0]["entity"]
        self.assertEqual(entity["name"], "orders")
        self.assertEqual(entity["type"], "dataset")
        self.assertEqual(entity["platform"], "dbt")

    def test_normalizes_entity_envelope_owners_and_governance(self) -> None:
        result = normalize_official_result(
            "get_entities",
            {
                "result": [
                    {
                        "urn": "urn:li:chart:revenue",
                        "properties": {
                            "name": "Revenue chart",
                            "customProperties": [
                                {"key": "business_critical", "value": "true"},
                                {"key": "contains_pii", "value": "true"},
                            ],
                        },
                        "ownership": {
                            "owners": [
                                {
                                    "owner": {
                                        "urn": "urn:li:corpuser:analyst",
                                        "properties": {"email": "analyst@example.com"},
                                    }
                                }
                            ]
                        },
                    }
                ]
            },
        )

        self.assertEqual(result[0]["name"], "Revenue chart")
        self.assertEqual(result[0]["type"], "chart")
        self.assertEqual(result[0]["owners"], ["analyst@example.com"])
        self.assertEqual(result[0]["tags"], ["critical", "pii"])

    def test_normalizes_schema_field_shape(self) -> None:
        result = normalize_official_result(
            "list_schema_fields",
            {
                "fields": [
                    {
                        "fieldPath": "order_id",
                        "nativeDataType": "NUMBER",
                        "tags": [
                            {
                                "tag": {
                                    "properties": {"name": "PrimaryKey"},
                                }
                            }
                        ],
                    }
                ]
            },
        )

        self.assertEqual(result["fields"][0]["name"], "order_id")
        self.assertEqual(result["fields"][0]["type"], "NUMBER")
        self.assertEqual(result["fields"][0]["tags"], ["PrimaryKey"])


if __name__ == "__main__":
    unittest.main()
