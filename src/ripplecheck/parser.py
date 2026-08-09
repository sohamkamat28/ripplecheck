"""Parse a constrained natural-language schema change into a stable request."""

from __future__ import annotations

import re

from .models import ChangeRequest


DATASET = r"(?P<dataset>[A-Za-z0-9_.-]+)"
COLUMN = r"[`\"']?(?P<column>[A-Za-z_][A-Za-z0-9_]*)[`\"']?"


DDL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "rename",
        re.compile(
            rf"^ALTER\s+TABLE\s+{DATASET}\s+RENAME\s+COLUMN\s+{COLUMN}\s+TO\s+"
            rf"[`\"']?(?P<replacement>[A-Za-z_][A-Za-z0-9_]*)[`\"']?\s*;?$",
            re.IGNORECASE,
        ),
    ),
    (
        "drop",
        re.compile(
            rf"^ALTER\s+TABLE\s+{DATASET}\s+DROP\s+COLUMN\s+{COLUMN}\s*;?$",
            re.IGNORECASE,
        ),
    ),
    (
        "type_change",
        re.compile(
            rf"^ALTER\s+TABLE\s+{DATASET}\s+ALTER\s+COLUMN\s+{COLUMN}\s+"
            rf"SET\s+DATA\s+TYPE\s+(?P<target_type>[A-Za-z0-9_(), ]+)\s*;?$",
            re.IGNORECASE,
        ),
    ),
)


PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "drop",
        re.compile(
            rf"\b(?:drop|remove)\s+(?:the\s+)?(?:column\s+)?{COLUMN}\s+(?:from|in)\s+{DATASET}",
            re.IGNORECASE,
        ),
    ),
    (
        "rename",
        re.compile(
            rf"\brename\s+(?:the\s+)?(?:column\s+)?{COLUMN}\s+to\s+"
            rf"[`\"']?(?P<replacement>[A-Za-z_][A-Za-z0-9_]*)[`\"']?\s+(?:in|on)\s+{DATASET}",
            re.IGNORECASE,
        ),
    ),
    (
        "type_change",
        re.compile(
            rf"\bchange\s+(?:the\s+)?type\s+of\s+(?:column\s+)?{COLUMN}\s+(?:in|on)\s+"
            rf"{DATASET}\s+to\s+(?P<target_type>[A-Za-z0-9_(), ]+)",
            re.IGNORECASE,
        ),
    ),
    (
        "deprecate",
        re.compile(
            rf"\bdeprecate\s+(?:the\s+)?(?:column\s+)?{COLUMN}\s+(?:from|in|on)\s+{DATASET}",
            re.IGNORECASE,
        ),
    ),
)


def parse_change_request(text: str) -> ChangeRequest:
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        raise ValueError("Describe a schema change before running the assessment.")

    for action, pattern in DDL_PATTERNS + PATTERNS:
        match = pattern.search(cleaned)
        if not match:
            continue
        values = match.groupdict()
        return ChangeRequest(
            raw=cleaned,
            action=action,
            dataset=values["dataset"].rstrip(".,"),
            column=values["column"],
            replacement=values.get("replacement"),
            target_type=(values.get("target_type") or "").strip(" .,;") or None,
        )

    raise ValueError(
        "Use Snowflake DDL or a supported request such as: ALTER TABLE "
        "warehouse.analytics.customer_360 RENAME COLUMN customer_tier TO loyalty_tier;"
    )
