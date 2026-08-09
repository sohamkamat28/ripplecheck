"""Deterministic orchestration over DataHub MCP metadata tools."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .intelligence import compile_intelligence
from .models import Assessment, ChangeRequest, ToolTrace
from .parser import parse_change_request
from .transport import DataHubTools


BREAKING_ACTIONS = {"drop", "rename", "type_change"}


class RipplecheckAgent:
    def __init__(self, tools: DataHubTools):
        self.tools = tools

    def assess(self, text: str, writeback: bool = True) -> dict[str, Any]:
        request = parse_change_request(text)
        trace: list[ToolTrace] = []

        search = self._call(
            trace,
            "search",
            {"query": search_query(request.dataset), "num_results": 8},
            "Resolved the proposed dataset against the DataHub catalog.",
        )
        source = select_source(search, request.dataset)
        if source is None:
            raise ValueError(f"Dataset not found in DataHub: {request.dataset}")

        schema = self._call(
            trace,
            "list_schema_fields",
            {"urn": source["urn"], "keywords": [request.column], "limit": 20},
            f"Confirmed whether column {request.column} exists and loaded its governance tags.",
        )
        field = select_field(schema, request.column)
        if field is None:
            raise ValueError(f"Column {request.column} was not found on {source['name']}.")

        lineage = self._call(
            trace,
            "get_lineage",
            {
                "urn": source["urn"],
                "column": request.column,
                "upstream": False,
                "max_hops": 3,
                "max_results": 50,
            },
            "Traced column-level downstream lineage through three hops.",
        )
        lineage_items = downstream_items(lineage)
        urns = [item.get("entity", {}).get("urn") for item in lineage_items]
        urns = [urn for urn in urns if urn]
        entities: list[dict[str, Any]] = []
        if urns:
            details = self._call(
                trace,
                "get_entities",
                {"urns": urns},
                "Loaded downstream owners, criticality tags, and asset types in one batch.",
            )
            entities = details if isinstance(details, list) else [details]

        blast_radius = build_blast_radius(lineage_items, entities, source)
        decision, risk_score, rationale = decide(request, source, field, blast_radius)
        owners = sorted(
            {
                owner
                for asset in blast_radius
                for owner in asset.get("owners", [])
                if isinstance(owner, str) and owner
            }
        )
        plan = remediation_plan(request, decision, owners)
        run_id = hashlib.sha256(request.raw.lower().encode("utf-8")).hexdigest()[:10]
        headline = decision_headline(request, decision, blast_radius)
        intelligence = compile_intelligence(
            request,
            source,
            field,
            blast_radius,
            decision,
            catalog_snapshot=self.tools.catalog_snapshot,
            transport_mode=self.tools.mode,
        )

        writeback_result: dict[str, Any]
        if writeback:
            record = decision_record(
                run_id,
                request,
                decision,
                risk_score,
                blast_radius,
                owners,
                intelligence["change_capsule"],
                intelligence["release_gate"],
            )
            writeback_result = self._call(
                trace,
                "update_description",
                {
                    "entity_urn": source["urn"],
                    "operation": "append",
                    "description": record,
                    "column_path": request.column,
                },
                "Appended the assessment to the source column so the next agent inherits it.",
            )
        else:
            writeback_result = {
                "success": False,
                "skipped": True,
                "message": "Writeback disabled for this run.",
            }

        assessment = Assessment(
            run_id=run_id,
            request=request_to_dict(request),
            decision=decision,
            risk_score=risk_score,
            headline=headline,
            rationale=rationale,
            source={**source, "field": field},
            blast_radius=blast_radius,
            owners_to_notify=owners,
            remediation_plan=plan,
            counterfactual=intelligence["counterfactual"],
            policy_proof=intelligence["policy_proof"],
            execution_plan=intelligence["execution_plan"],
            artifact_manifest=intelligence["artifact_manifest"],
            change_capsule=intelligence["change_capsule"],
            release_gate=intelligence["release_gate"],
            tool_trace=trace,
            writeback=writeback_result,
        )
        return assessment.to_dict()

    def _call(
        self,
        trace: list[ToolTrace],
        name: str,
        arguments: dict[str, Any],
        summary: str,
    ) -> Any:
        result = self.tools.call_tool(name, arguments)
        trace.append(ToolTrace(tool=name, arguments=arguments, summary=summary))
        return result


def search_query(dataset: str) -> str:
    tokens = [token for token in dataset.replace("-", "_").split(".") if token]
    return "/q " + "+".join(tokens)


def select_source(search: dict[str, Any], dataset: str) -> dict[str, Any] | None:
    results = search.get("searchResults") or search.get("search_results") or []
    candidates = [item.get("entity", item) for item in results if isinstance(item, dict)]
    wanted = dataset.lower()
    for entity in candidates:
        if str(entity.get("name", "")).lower() == wanted:
            return entity
    return candidates[0] if candidates else None


def select_field(schema: dict[str, Any], column: str) -> dict[str, Any] | None:
    fields = schema.get("fields", [])
    for field in fields:
        name = field.get("name") or field.get("fieldPath") or field.get("field_path")
        if str(name).lower() == column.lower():
            return {**field, "name": name}
    return None


def downstream_items(lineage: dict[str, Any]) -> list[dict[str, Any]]:
    downstream = lineage.get("downstreams", {})
    if isinstance(downstream, list):
        return downstream
    return downstream.get("searchResults") or downstream.get("search_results") or []


def build_blast_radius(
    lineage_items: list[dict[str, Any]],
    details: list[dict[str, Any]],
    source: dict[str, Any],
) -> list[dict[str, Any]]:
    detail_map = {item.get("urn"): item for item in details}
    name_map = {
        source.get("urn"): source.get("name", source.get("urn")),
        **{
            item.get("urn"): item.get("name", item.get("urn"))
            for item in details
            if item.get("urn")
        },
    }
    assets = []
    for item in lineage_items:
        compact = item.get("entity", item)
        urn = compact.get("urn")
        entity = {**compact, **detail_map.get(urn, {})}
        raw_path = item.get("path") or [source.get("urn"), urn]
        lineage_path = [name_map.get(path_urn, path_urn) for path_urn in raw_path if path_urn]
        assets.append(
            {
                "urn": urn,
                "name": entity.get("name", urn),
                "type": entity.get("type", "dataset"),
                "platform": entity.get("platform", "unknown"),
                "degree": int(item.get("degree", 1)),
                "owners": entity.get("owners", []),
                "tags": entity.get("tags", []),
                "impact": impact_label(entity),
                "lineage_path": lineage_path,
            }
        )
    assets.sort(key=lambda value: (value["degree"], value["type"], value["name"]))
    return assets


def impact_label(entity: dict[str, Any]) -> str:
    entity_type = str(entity.get("type", "dataset")).lower()
    if entity_type in {"dashboard", "chart"}:
        return "Executive metric may fail or become stale"
    if entity_type in {"mlmodel", "ml_model"}:
        return "Production feature input may drift or disappear"
    if entity_type in {"dataflow", "pipeline"}:
        return "Scheduled transformation may fail"
    return "Derived dataset may fail to build"


def decide(
    request: ChangeRequest,
    source: dict[str, Any],
    field: dict[str, Any],
    blast_radius: list[dict[str, Any]],
) -> tuple[str, int, list[str]]:
    tags = {str(tag).lower() for tag in source.get("tags", []) + field.get("tags", [])}
    critical_assets = [
        asset
        for asset in blast_radius
        if any(str(tag).lower() == "critical" for tag in asset.get("tags", []))
    ]
    dashboards = [
        asset
        for asset in blast_radius
        if asset["type"].lower() in {"dashboard", "chart"}
    ]
    models = [
        asset for asset in blast_radius if asset["type"].lower() in {"mlmodel", "ml_model"}
    ]
    unowned = [asset for asset in blast_radius if not asset.get("owners")]
    score = min(
        10,
        len(blast_radius)
        + len(critical_assets) * 2
        + len(dashboards)
        + len(models) * 2
        + len(unowned)
        + (2 if "pii" in tags else 0),
    )

    if request.action in BREAKING_ACTIONS and blast_radius:
        decision = "BLOCK"
    elif request.action == "deprecate" and blast_radius:
        decision = "REVIEW"
    else:
        decision = "SAFE"

    rationale = []
    if blast_radius:
        rationale.append(
            f"DataHub column lineage found {len(blast_radius)} downstream assets across "
            f"{max(asset['degree'] for asset in blast_radius)} hops."
        )
    else:
        rationale.append("DataHub returned no downstream dependencies for this column.")
    if critical_assets:
        rationale.append(
            count_sentence(len(critical_assets), "affected asset is", "affected assets are")
            + " tagged Critical."
        )
    if dashboards:
        rationale.append(
            count_sentence(
                len(dashboards),
                "affected dashboard exposes",
                "affected dashboards expose",
            )
            + " the change to consumers."
        )
    if models:
        rationale.append(
            count_sentence(
                len(models), "production ML asset consumes", "production ML assets consume"
            )
            + " the column."
        )
    if "pii" in tags:
        rationale.append("The source column carries a PII governance tag.")
    if unowned:
        rationale.append(
            count_sentence(len(unowned), "affected asset has", "affected assets have")
            + " no owner recorded in DataHub."
        )
    return decision, score, rationale


def remediation_plan(request: ChangeRequest, decision: str, owners: list[str]) -> list[str]:
    if decision == "SAFE":
        return [
            "Proceed through the normal schema-change review.",
            "Run contract tests and refresh DataHub lineage after deployment.",
        ]

    plan = ["Pause the breaking migration before merge or deployment."]
    if request.action == "rename" and request.replacement:
        plan.append(
            f"Add {request.replacement} beside {request.column} and maintain both during migration."
        )
    elif request.action == "type_change" and request.target_type:
        plan.append(
            f"Introduce a compatible cast into a new column before changing to {request.target_type}."
        )
    else:
        plan.append(f"Deprecate {request.column} and keep a compatibility window before removal.")
    if owners:
        plan.append("Notify: " + ", ".join(owners) + ".")
    plan.append("Update downstream assets, then rerun Ripplecheck until the decision is SAFE.")
    return plan


def decision_headline(
    request: ChangeRequest, decision: str, blast_radius: list[dict[str, Any]]
) -> str:
    verb = {
        "drop": "Dropping",
        "rename": "Renaming",
        "type_change": "Changing the type of",
        "deprecate": "Deprecating",
    }[request.action]
    if decision == "BLOCK":
        return f"Block the change. {verb} {request.column} impacts {len(blast_radius)} assets."
    if decision == "REVIEW":
        return f"Review the rollout. {verb} {request.column} needs an owner-approved migration."
    return f"No downstream blockers found for {request.column}."


def decision_record(
    run_id: str,
    request: ChangeRequest,
    decision: str,
    risk_score: int,
    blast_radius: list[dict[str, Any]],
    owners: list[str],
    change_capsule: dict[str, Any],
    release_gate: dict[str, Any],
) -> str:
    payload = {
        "run_id": run_id,
        "decision": decision,
        "risk_score": risk_score,
        "proposed_change": request.raw,
        "downstream_assets": [asset["urn"] for asset in blast_radius],
        "owners_to_notify": owners,
        "capsule_id": change_capsule["capsule_id"],
        "evidence_sha256": change_capsule["evidence_sha256"],
        "release_gate": release_gate["status"],
        "policy_blockers": release_gate["blockers"],
    }
    return "\n\n### Ripplecheck decision\n```json\n" + json.dumps(payload, indent=2) + "\n```"


def request_to_dict(request: ChangeRequest) -> dict[str, Any]:
    return {
        "raw": request.raw,
        "action": request.action,
        "dataset": request.dataset,
        "column": request.column,
        "replacement": request.replacement,
        "target_type": request.target_type,
    }


def count_sentence(count: int, singular: str, plural: str) -> str:
    return f"{count} {singular if count == 1 else plural}"
