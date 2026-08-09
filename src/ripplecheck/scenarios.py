"""Curated demo prompts used by the CLI and web interface."""

SCENARIOS = [
    {
        "id": "customer-tier-rename",
        "label": "Rename a production contract",
        "change": (
            "ALTER TABLE warehouse.analytics.customer_360 "
            "RENAME COLUMN customer_tier TO loyalty_tier;"
        ),
        "expected": "BLOCK",
    },
    {
        "id": "revenue-rename",
        "label": "Rename a finance metric",
        "change": (
            "ALTER TABLE warehouse.finance.monthly_revenue "
            "RENAME COLUMN net_revenue TO recognized_revenue;"
        ),
        "expected": "BLOCK",
    },
    {
        "id": "safe-sandbox-drop",
        "label": "Remove an unused sandbox field",
        "change": "Drop column legacy_bucket from warehouse.sandbox.experiment_flags",
        "expected": "SAFE",
    },
]
