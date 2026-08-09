"""Regenerate checked-in sample outputs from the real agent path."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ripplecheck.agent import RipplecheckAgent  # noqa: E402
from ripplecheck.evidence_pack import evidence_files  # noqa: E402
from ripplecheck.scenarios import SCENARIOS  # noqa: E402
from ripplecheck.transport import FixtureDataHubTools  # noqa: E402


def main() -> None:
    output_dir = ROOT / "samples"
    output_dir.mkdir(exist_ok=True)
    tools = FixtureDataHubTools(ROOT / "data" / "catalog.json")
    agent = RipplecheckAgent(tools)
    for scenario in SCENARIOS:
        result = agent.assess(scenario["change"], writeback=True)
        path = output_dir / f"{scenario['id']}.json"
        path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
        example_dir = ROOT / "examples" / scenario["id"]
        for relative_path, content in evidence_files(result).items():
            artifact_path = example_dir / relative_path
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text(content, encoding="utf-8")
            print(artifact_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
