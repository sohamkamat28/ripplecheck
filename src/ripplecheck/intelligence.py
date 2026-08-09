"""Compile DataHub evidence into a deterministic migration proof and plan."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import ChangeRequest


def compile_intelligence(
    request: ChangeRequest,
    source: dict[str, Any],
    field: dict[str, Any],
    blast_radius: list[dict[str, Any]],
    decision: str,
) -> dict[str, Any]:
    """Project the proposed change without mutation and compile review artifacts."""
    counterfactual = build_counterfactual(request, field, blast_radius)
    policy_proof = build_policy_proof(request, source, field, blast_radius)
    release_gate = build_release_gate(policy_proof, decision)
    execution_plan = build_execution_plan(request, blast_radius, release_gate)
    artifact_manifest = build_artifact_manifest(request)
    change_capsule = build_change_capsule(
        request,
        source,
        field,
        blast_radius,
        policy_proof,
        release_gate,
    )
    return {
        "counterfactual": counterfactual,
        "policy_proof": policy_proof,
        "release_gate": release_gate,
        "execution_plan": execution_plan,
        "artifact_manifest": artifact_manifest,
        "change_capsule": change_capsule,
    }


def build_counterfactual(
    request: ChangeRequest,
    field: dict[str, Any],
    blast_radius: list[dict[str, Any]],
) -> dict[str, Any]:
    critical = [asset for asset in blast_radius if has_tag(asset, "critical")]
    owned = [asset for asset in blast_radius if asset.get("owners")]
    max_hops = max((asset["degree"] for asset in blast_radius), default=0)
    replacement = projected_field_name(request)
    after_status = "removed" if request.action == "drop" else "renamed"
    if request.action == "type_change":
        after_status = "type changed"
    elif request.action == "deprecate":
        after_status = "deprecated"

    failures = []
    for asset in blast_radius:
        failures.append(
            {
                "asset": asset["name"],
                "type": asset["type"],
                "severity": "critical" if has_tag(asset, "critical") else "high",
                "failure_mode": failure_mode(asset, request),
                "lineage_path": asset.get("lineage_path", []),
                "owner": (asset.get("owners") or ["UNOWNED"])[0],
            }
        )

    total = len(blast_radius)
    coverage = round((len(owned) / total) * 100) if total else 100
    return {
        "engine": "metadata-graph-counterfactual/v1",
        "mode": "non-mutating projection",
        "before": {
            "field": request.column,
            "type": field.get("type", "unknown"),
            "status": "present",
            "consumer_edges": total,
        },
        "after": {
            "field": replacement,
            "type": request.target_type or field.get("type", "unknown"),
            "status": after_status,
            "broken_edges": total if request.action in {"drop", "rename", "type_change"} else 0,
        },
        "metrics": {
            "assets_inspected": total,
            "broken_edges": total if request.action in {"drop", "rename", "type_change"} else 0,
            "critical_consumers": len(critical),
            "max_lineage_hops": max_hops,
            "owned_assets": len(owned),
            "ownership_coverage": coverage,
        },
        "predicted_failures": failures,
    }


def build_policy_proof(
    request: ChangeRequest,
    source: dict[str, Any],
    field: dict[str, Any],
    blast_radius: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    breaking = request.action in {"drop", "rename", "type_change"}
    critical = [asset for asset in blast_radius if has_tag(asset, "critical")]
    unowned = [asset for asset in blast_radius if not asset.get("owners")]
    production_models = [
        asset
        for asset in blast_radius
        if asset["type"].lower() in {"mlmodel", "ml_model"}
        and has_tag(asset, "production")
    ]
    governed = sorted(
        {
            str(tag)
            for tag in source.get("tags", []) + field.get("tags", [])
            if str(tag).lower() in {"critical", "pii", "financial", "tier1"}
        }
    )
    return [
        policy(
            "RC-001",
            "Breaking changes need zero active consumers",
            "FAIL" if breaking and blast_radius else "PASS",
            f"{len(blast_radius)} active column-lineage edges found across the inspected graph.",
        ),
        policy(
            "RC-007",
            "Critical consumers require an explicit migration",
            "FAIL" if breaking and critical else "PASS",
            f"{len(critical)} affected assets carry the Critical tag.",
        ),
        policy(
            "RC-013",
            "Every affected asset must have an accountable owner",
            "WARN" if unowned else "PASS",
            (
                f"{len(unowned)} affected asset has no DataHub owner."
                if len(unowned) == 1
                else f"{len(unowned)} affected assets have no DataHub owner."
            ),
        ),
        policy(
            "RC-021",
            "Production ML inputs cannot change without feature migration",
            "FAIL" if breaking and production_models else "PASS",
            f"{len(production_models)} production ML consumer uses the proposed field.",
        ),
        policy(
            "RC-032",
            "The rollout must be backward compatible and reversible",
            "FAIL" if breaking and blast_radius else "PASS",
            (
                "Direct DDL has no compatibility window or rollback gate."
                if breaking and blast_radius
                else "No incompatible downstream edge was found."
            ),
        ),
        policy(
            "RC-044",
            "Governed fields require catalog evidence",
            "PASS",
            "DataHub evidence loaded" + (f" for tags: {', '.join(governed)}." if governed else "."),
        ),
    ]


def build_release_gate(
    policy_proof: list[dict[str, Any]], decision: str
) -> dict[str, Any]:
    blockers = [item["id"] for item in policy_proof if item["status"] == "FAIL"]
    warnings = [item["id"] for item in policy_proof if item["status"] == "WARN"]
    return {
        "status": "CLOSED" if blockers or decision == "BLOCK" else "OPEN",
        "blockers": blockers,
        "warnings": warnings,
        "passed": [item["id"] for item in policy_proof if item["status"] == "PASS"],
        "required_approvals": ["data owner", "downstream owners"] if blockers else [],
        "release_condition": (
            "Migrate every active consumer, reach 100% ownership, and rerun this capsule."
            if blockers
            else "Evidence satisfies the bounded schema-change policy."
        ),
    }


def build_execution_plan(
    request: ChangeRequest,
    blast_radius: list[dict[str, Any]],
    release_gate: dict[str, Any],
) -> list[dict[str, Any]]:
    new_field = projected_field_name(request)
    introduce_action = f"Introduce {new_field}"
    introduce_evidence = (
        f"Add {new_field} beside {request.column}; do not remove the old contract."
    )
    if request.action in {"drop", "deprecate"}:
        introduce_action = f"Deprecate {request.column} in contracts"
        introduce_evidence = (
            f"Keep {request.column} available while downstream consumers migrate or attest non-use."
        )
    plan = [
        node(
            "G0",
            "Freeze direct DDL",
            [],
            "Ripplecheck policy",
            "blocked" if release_gate["status"] == "CLOSED" else "ready",
            "Prevent the breaking statement from entering the deploy queue.",
        ),
        node(
            "M1",
            introduce_action,
            ["G0"],
            "data-platform@northstar.example",
            "ready",
            introduce_evidence,
        ),
        node(
            "M2",
            "Publish compatibility layer",
            ["M1"],
            "data-platform@northstar.example",
            "ready",
            "Dual-read both names and backfill until parity is proven.",
        ),
    ]
    migration_ids = []
    for index, asset in enumerate(blast_radius, start=1):
        migration_id = f"C{index}"
        migration_ids.append(migration_id)
        plan.append(
            node(
                migration_id,
                f"Migrate {asset['name']}",
                ["M2"],
                (asset.get("owners") or ["owner required"])[0],
                "waiting",
                failure_mode(asset, request),
            )
        )
    plan.extend(
        [
            node(
                "V1",
                "Prove parity and lineage convergence",
                migration_ids or ["M2"],
                "release automation",
                "waiting",
                "Require zero failed consumers, contract-test parity, and a fresh DataHub lineage run.",
            ),
            node(
                "G1",
                f"Retire {request.column}",
                ["V1"],
                "data owner approval",
                "approval required",
                "Open the release gate only after the compatibility window and rollback check pass.",
            ),
        ]
    )
    return plan


def build_artifact_manifest(request: ChangeRequest) -> list[dict[str, Any]]:
    model_name = request.dataset.split(".")[-1]
    files = [
        ("migration/compatibility_view.sql", "Zero-downtime compatibility SQL"),
        (f"models/{model_name}/schema.yml", "dbt model contract patch"),
        (f"tests/assert_{request.column}_compatibility.sql", "Parity gate test"),
        ("review/ripplecheck-decision.md", "Human-readable PR decision"),
        ("review/owner-routing.json", "Machine-readable owner routing"),
        ("manifest/change-capsule.json", "Reproducible evidence manifest"),
    ]
    return [
        {"path": path, "purpose": purpose, "status": "generated"}
        for path, purpose in files
    ]


def build_change_capsule(
    request: ChangeRequest,
    source: dict[str, Any],
    field: dict[str, Any],
    blast_radius: list[dict[str, Any]],
    policy_proof: list[dict[str, Any]],
    release_gate: dict[str, Any],
) -> dict[str, Any]:
    evidence = {
        "request": {
            "action": request.action,
            "dataset": request.dataset,
            "column": request.column,
            "replacement": request.replacement,
            "target_type": request.target_type,
        },
        "source_urn": source.get("urn"),
        "field_type": field.get("type"),
        "consumer_urns": [asset.get("urn") for asset in blast_radius],
        "policies": [{"id": item["id"], "status": item["status"]} for item in policy_proof],
        "gate": release_gate["status"],
    }
    canonical = json.dumps(evidence, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    graph = json.dumps(
        [
            {
                "urn": asset.get("urn"),
                "path": asset.get("lineage_path", []),
                "owners": asset.get("owners", []),
                "tags": asset.get("tags", []),
            }
            for asset in blast_radius
        ],
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "capsule_id": f"RC-{digest[:12].upper()}",
        "schema_version": "1.0",
        "compiler": "ripplecheck/2.0",
        "deterministic": True,
        "input_sha256": digest,
        "evidence_sha256": hashlib.sha256(graph.encode("utf-8")).hexdigest(),
        "catalog_snapshot": "retail-analytics-demo",
        "transport": "DataHub MCP tool contract",
    }


def projected_field_name(request: ChangeRequest) -> str:
    if request.action == "rename" and request.replacement:
        return request.replacement
    if request.action == "drop":
        return "REMOVED"
    if request.action == "type_change":
        return f"{request.column}_v2"
    return request.column


def failure_mode(asset: dict[str, Any], request: ChangeRequest) -> str:
    name = request.column
    entity_type = asset["type"].lower()
    if entity_type == "dashboard":
        return f"Metric query references {name}; tiles can error or serve stale data."
    if entity_type in {"mlmodel", "ml_model"}:
        return f"Online feature contract loses {name}; training-serving skew is possible."
    if entity_type in {"dataflow", "pipeline"}:
        return f"Scheduled transformation references {name}; task compilation can fail."
    return f"Model contract still selects {name}; dbt compilation can fail."


def has_tag(asset: dict[str, Any], tag: str) -> bool:
    return any(str(value).lower() == tag.lower() for value in asset.get("tags", []))


def policy(rule_id: str, title: str, status: str, evidence: str) -> dict[str, Any]:
    return {"id": rule_id, "title": title, "status": status, "evidence": evidence}


def node(
    node_id: str,
    action: str,
    depends_on: list[str],
    actor: str,
    state: str,
    evidence: str,
) -> dict[str, Any]:
    return {
        "id": node_id,
        "action": action,
        "depends_on": depends_on,
        "actor": actor,
        "state": state,
        "evidence": evidence,
    }
