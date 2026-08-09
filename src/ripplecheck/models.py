"""Small, dependency-free domain models used by the agent."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ChangeRequest:
    raw: str
    action: str
    dataset: str
    column: str
    replacement: str | None = None
    target_type: str | None = None


@dataclass
class ToolTrace:
    tool: str
    arguments: dict[str, Any]
    summary: str


@dataclass
class Assessment:
    run_id: str
    request: dict[str, Any]
    decision: str
    risk_score: int
    headline: str
    rationale: list[str]
    source: dict[str, Any]
    blast_radius: list[dict[str, Any]]
    owners_to_notify: list[str]
    remediation_plan: list[str]
    counterfactual: dict[str, Any]
    policy_proof: list[dict[str, Any]]
    execution_plan: list[dict[str, Any]]
    artifact_manifest: list[dict[str, Any]]
    change_capsule: dict[str, Any]
    release_gate: dict[str, Any]
    tool_trace: list[ToolTrace] = field(default_factory=list)
    writeback: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["tool_trace"] = [asdict(item) for item in self.tool_trace]
        return value
