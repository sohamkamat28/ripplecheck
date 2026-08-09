"""Fast submission audit for required files and checked-in samples."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "LICENSE",
    "README.md",
    "Dockerfile",
    "render.yaml",
    "vercel.json",
    "api/index.py",
    "public/index.html",
    "public/robots.txt",
    "public/llms.txt",
    "data/catalog.json",
    "docs/DEVPOST.md",
    "docs/DEVPOST_FORM.md",
    "docs/TESTING.md",
    "docs/RULES_COMPLIANCE.md",
    "docs/DISCLOSURES.md",
    "docs/LIVE_DATAHUB_PROOF.md",
    "docs/DEMO_SCRIPT.md",
    "docs/DEMO_RUNBOOK.md",
    "docs/ARCHITECTURE.md",
    "docs/ripplecheck-result.png",
    "samples/customer-tier-rename.json",
    "samples/revenue-rename.json",
    "samples/safe-sandbox-drop.json",
    "samples/live-datahub-proof.json",
    "examples/customer-tier-rename/migration/compatibility_view.sql",
    "examples/customer-tier-rename/models/customer_360/schema.yml",
    "examples/customer-tier-rename/tests/assert_customer_tier_compatibility.sql",
    "examples/customer-tier-rename/review/ripplecheck-decision.md",
    "examples/customer-tier-rename/review/owner-routing.json",
    "examples/customer-tier-rename/manifest/change-capsule.json",
]


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("Missing required files: " + ", ".join(missing))
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if "Apache License" not in license_text or "Version 2.0" not in license_text:
        raise SystemExit("LICENSE is not Apache 2.0")
    public_copy = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ("public/index.html", "public/app.js")
    )
    if "—" in public_copy or "–" in public_copy:
        raise SystemExit("Public UI contains a disallowed long dash character")
    script_lines = (ROOT / "docs" / "DEMO_RUNBOOK.md").read_text(encoding="utf-8").splitlines()
    narration_words = sum(len(line.split()) for line in script_lines if line.startswith('"'))
    if narration_words > 390:
        raise SystemExit(f"Demo narration is too long: {narration_words} words")
    for path in sorted((ROOT / "samples").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if path.name == "live-datahub-proof.json":
            if payload.get("writeback", {}).get("success") is not True:
                raise SystemExit("live-datahub-proof.json is missing successful writeback proof")
            if payload.get("tool_trace", [])[-1:] != ["update_description"]:
                raise SystemExit("live-datahub-proof.json is missing the mutation tool trace")
            continue
        for key in (
            "decision",
            "blast_radius",
            "counterfactual",
            "policy_proof",
            "execution_plan",
            "artifact_manifest",
            "change_capsule",
            "release_gate",
            "tool_trace",
            "writeback",
        ):
            if key not in payload:
                raise SystemExit(f"{path.name} is missing {key}")
    placeholders = (ROOT / "docs" / "DEVPOST.md").read_text(encoding="utf-8")
    if "<your-handle>" in placeholders:
        raise SystemExit("docs/DEVPOST.md still contains a repository placeholder")
    print("submission preflight: ok")


if __name__ == "__main__":
    main()
