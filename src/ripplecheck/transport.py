"""DataHub MCP transports: a local fixture and the official stdio server."""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
import shlex
import subprocess
import threading
from typing import Any


class DataHubTools(ABC):
    mode = "unknown"
    catalog_snapshot = "unknown"

    @abstractmethod
    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Call one DataHub MCP tool and return its structured result."""

    def close(self) -> None:
        """Release transport resources."""


class FixtureDataHubTools(DataHubTools):
    """Implements the official tool names over a realistic metadata snapshot."""

    mode = "fixture"
    catalog_snapshot = "retail-analytics-demo"

    def __init__(self, catalog_path: Path, state_path: Path | None = None):
        self.catalog_path = catalog_path
        self.state_path = state_path
        self.catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        self.entities = {entity["urn"]: entity for entity in self.catalog["entities"]}
        self.writes: list[dict[str, Any]] = self._load_writes()
        self._lock = threading.Lock()
        for record in self.writes:
            self._apply_description(record)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        handler = getattr(self, f"_tool_{name}", None)
        if handler is None:
            raise ValueError(f"Fixture does not implement DataHub MCP tool: {name}")
        return handler(arguments)

    def _tool_search(self, arguments: dict[str, Any]) -> dict[str, Any]:
        query = str(arguments.get("query", "*")).lower()
        terms = [
            term
            for term in re_tokenize(query.replace("/q", ""))
            if term not in {"and", "or", "not", "q"}
        ]
        scored: list[tuple[int, dict[str, Any]]] = []
        for entity in self.entities.values():
            haystack = " ".join(
                [
                    entity.get("name", ""),
                    entity.get("urn", ""),
                    entity.get("description", ""),
                    " ".join(field.get("name", "") for field in entity.get("fields", [])),
                ]
            ).lower()
            score = sum(1 for term in terms if term in haystack)
            if query.strip() in {"*", "/q *"} or score:
                scored.append((score, entity))
        scored.sort(key=lambda item: (-item[0], item[1].get("name", "")))
        limit = min(int(arguments.get("num_results", 10)), 50)
        results = [
            {"entity": compact_entity(entity), "score": score}
            for score, entity in scored[:limit]
        ]
        return {"searchResults": results, "total": len(scored), "mode": "fixture"}

    def _tool_list_schema_fields(self, arguments: dict[str, Any]) -> dict[str, Any]:
        urn = str(arguments["urn"])
        entity = self._require_entity(urn)
        keywords = [str(value).lower() for value in arguments.get("keywords") or []]
        fields = entity.get("fields", [])
        if keywords:
            fields = [
                field
                for field in fields
                if any(
                    keyword
                    in " ".join(
                        [
                            field.get("name", ""),
                            field.get("description", ""),
                            " ".join(field.get("tags", [])),
                        ]
                    ).lower()
                    for keyword in keywords
                )
            ]
        offset = int(arguments.get("offset", 0))
        limit = int(arguments.get("limit", 100))
        page = fields[offset : offset + limit]
        return {
            "urn": urn,
            "fields": page,
            "totalFields": len(entity.get("fields", [])),
            "matchingCount": len(fields) if keywords else None,
            "returned": len(page),
            "offset": offset,
        }

    def _tool_get_lineage(self, arguments: dict[str, Any]) -> dict[str, Any]:
        urn = str(arguments["urn"])
        column = arguments.get("column")
        upstream = bool(arguments.get("upstream", True))
        max_hops = max(1, min(int(arguments.get("max_hops", 1)), 3))
        if upstream:
            return {"upstreams": {"searchResults": []}, "downstreams": {"searchResults": []}}

        visited = {urn}
        frontier = [(urn, 0, [urn])]
        collected: list[dict[str, Any]] = []
        while frontier:
            current_urn, degree, path = frontier.pop(0)
            if degree >= max_hops:
                continue
            current = self._require_entity(current_urn)
            for edge in current.get("downstream", []):
                if degree == 0 and column and column not in edge.get("columns", []):
                    continue
                downstream_urn = edge["urn"]
                if downstream_urn in visited:
                    continue
                visited.add(downstream_urn)
                entity = self._require_entity(downstream_urn)
                collected.append(
                    {
                        "entity": compact_entity(entity),
                        "degree": degree + 1,
                        "lineageColumns": edge.get("columns", []),
                        "path": [*path, downstream_urn],
                    }
                )
                frontier.append((downstream_urn, degree + 1, [*path, downstream_urn]))
        return {
            "upstreams": {"searchResults": []},
            "downstreams": {
                "searchResults": collected,
                "total": len(collected),
                "returned": len(collected),
                "hasMore": False,
            },
            "mode": "fixture",
        }

    def _tool_get_entities(self, arguments: dict[str, Any]) -> dict[str, Any] | list[dict[str, Any]]:
        urns = arguments.get("urns", [])
        single = isinstance(urns, str)
        if single:
            urns = [urns]
        result = [self._require_entity(str(urn)) for urn in urns]
        return result[0] if single else result

    def _tool_update_description(self, arguments: dict[str, Any]) -> dict[str, Any]:
        urn = str(arguments["entity_urn"])
        self._require_entity(urn)
        record = {
            "entity_urn": urn,
            "operation": arguments.get("operation", "append"),
            "description": arguments.get("description", ""),
            "column_path": arguments.get("column_path"),
        }
        with self._lock:
            self.writes.append(record)
            self._apply_description(record)
            self._persist_writes()
        return {
            "success": True,
            "urn": urn,
            "column_path": record["column_path"],
            "message": (
                "Decision record appended to the offline DataHub run state."
                if self.state_path
                else "Decision record captured by the offline DataHub fixture."
            ),
            "mode": "fixture",
        }

    def _require_entity(self, urn: str) -> dict[str, Any]:
        if urn not in self.entities:
            raise ValueError(f"Entity not found: {urn}")
        return self.entities[urn]

    def _load_writes(self) -> list[dict[str, Any]]:
        if self.state_path is None or not self.state_path.is_file():
            return []
        try:
            value = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        writes = value.get("writes", []) if isinstance(value, dict) else []
        return writes if isinstance(writes, list) else []

    def _apply_description(self, record: dict[str, Any]) -> None:
        entity = self._require_entity(record["entity_urn"])
        column = record.get("column_path")
        target = entity
        if column:
            target = next(
                (
                    field
                    for field in entity.get("fields", [])
                    if field.get("name") == column or field.get("fieldPath") == column
                ),
                entity,
            )
        operation = record.get("operation", "append")
        if operation == "remove":
            target["description"] = ""
        elif operation == "replace":
            target["description"] = str(record.get("description", ""))
        else:
            target["description"] = (
                str(target.get("description", "")) + str(record.get("description", ""))
            )

    def _persist_writes(self) -> None:
        if self.state_path is None:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.state_path.with_suffix(self.state_path.suffix + ".tmp")
        temporary.write_text(
            json.dumps({"writes": self.writes}, indent=2) + "\n", encoding="utf-8"
        )
        temporary.replace(self.state_path)


class StdioMCPDataHubTools(DataHubTools):
    """Minimal MCP client for the official DataHub stdio server."""

    mode = "live"
    catalog_snapshot = "live-datahub"

    def __init__(self, command: str):
        args = shlex.split(command)
        if not args:
            raise ValueError("DATAHUB_MCP_COMMAND cannot be empty")
        self._process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=os.environ.copy(),
        )
        self._stderr_lines: list[str] = []
        self._stderr_thread = threading.Thread(target=self._drain_stderr, daemon=True)
        self._stderr_thread.start()
        self._next_id = 1
        self._lock = threading.Lock()
        self._request(
            "initialize",
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "ripplecheck", "version": "1.0.0"},
            },
        )
        self._notify("notifications/initialized", {})

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        result = self._request("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError"):
            raise RuntimeError(extract_text(result) or f"DataHub MCP tool {name} failed")
        structured = result.get("structuredContent")
        if isinstance(structured, dict):
            return normalize_official_result(name, structured)
        text = extract_text(result)
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"DataHub MCP tool {name} returned non-JSON content") from exc
        if not isinstance(value, (dict, list)):
            raise RuntimeError(f"DataHub MCP tool {name} returned an unsupported payload")
        return normalize_official_result(name, value)

    def close(self) -> None:
        if self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._process.kill()

    def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            request_id = self._next_id
            self._next_id += 1
            self._write({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
            while True:
                message = self._read()
                if message.get("id") != request_id:
                    continue
                if "error" in message:
                    raise RuntimeError(str(message["error"]))
                result = message.get("result", {})
                if not isinstance(result, dict):
                    raise RuntimeError(f"Unexpected MCP response for {method}")
                return result

    def _notify(self, method: str, params: dict[str, Any]) -> None:
        self._write({"jsonrpc": "2.0", "method": method, "params": params})

    def _write(self, payload: dict[str, Any]) -> None:
        if self._process.stdin is None:
            raise RuntimeError("DataHub MCP stdin is unavailable")
        self._process.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
        self._process.stdin.flush()

    def _read(self) -> dict[str, Any]:
        if self._process.stdout is None:
            raise RuntimeError("DataHub MCP stdout is unavailable")
        line = self._process.stdout.readline()
        if not line:
            details = "".join(self._stderr_lines[-20:]).strip()
            suffix = f": {details}" if details else ""
            raise RuntimeError(f"DataHub MCP server exited unexpectedly{suffix}")
        value = json.loads(line)
        if not isinstance(value, dict):
            raise RuntimeError("Invalid MCP response")
        return value

    def _drain_stderr(self) -> None:
        if self._process.stderr is None:
            return
        for line in self._process.stderr:
            self._stderr_lines.append(line)
            if len(self._stderr_lines) > 100:
                del self._stderr_lines[:-100]


def re_tokenize(value: str) -> list[str]:
    current = ""
    tokens: list[str] = []
    for char in value:
        if char.isalnum() or char in "_.-":
            current += char
        elif current:
            tokens.append(current)
            current = ""
    if current:
        tokens.append(current)
    return tokens


def normalize_official_result(name: str, value: Any) -> Any:
    """Map current DataHub MCP response envelopes to Ripplecheck's compact contract."""
    if name == "get_entities" and isinstance(value, dict) and "result" in value:
        value = value["result"]
    if name == "search" and isinstance(value, dict):
        for item in value.get("searchResults", []):
            if isinstance(item, dict) and isinstance(item.get("entity"), dict):
                item["entity"] = normalize_official_entity(item["entity"])
    elif name == "list_schema_fields" and isinstance(value, dict):
        value["fields"] = [
            normalize_official_field(field)
            for field in value.get("fields", [])
            if isinstance(field, dict)
        ]
    elif name == "get_lineage" and isinstance(value, dict):
        for direction in ("upstreams", "downstreams"):
            bucket = value.get(direction, {})
            items = bucket if isinstance(bucket, list) else bucket.get("searchResults", [])
            for item in items:
                if isinstance(item, dict) and isinstance(item.get("entity"), dict):
                    item["entity"] = normalize_official_entity(item["entity"])
    if isinstance(value, list):
        return [normalize_official_entity(item) if isinstance(item, dict) else item for item in value]
    if name == "get_entities" and isinstance(value, dict):
        return normalize_official_entity(value)
    return value


def normalize_official_field(field: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(field)
    normalized["name"] = field.get("name") or field.get("fieldPath")
    normalized["type"] = (
        field.get("type") or field.get("nativeDataType") or field.get("nativeType") or "unknown"
    )
    normalized["tags"] = collect_names(field.get("tags"))
    normalized["tags"].extend(str(term) for term in field.get("editedGlossaryTerms", []))
    normalized["tags"] = sorted(set(normalized["tags"]))
    return normalized


def normalize_official_entity(entity: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(entity)
    properties = entity.get("properties") if isinstance(entity.get("properties"), dict) else {}
    normalized["name"] = entity.get("name") or properties.get("name") or entity.get("urn")
    normalized["type"] = entity.get("type") or urn_entity_type(str(entity.get("urn", "")))
    platform = entity.get("platform")
    normalized["platform"] = (
        (platform.get("name") or platform.get("urn"))
        if isinstance(platform, dict)
        else (platform or "unknown")
    )

    owners = collect_owners(entity.get("ownership") or entity.get("owners"))
    custom = properties.get("customProperties", [])
    if isinstance(custom, list):
        for item in custom:
            if not isinstance(item, dict):
                continue
            key = str(item.get("key", "")).lower()
            value = str(item.get("value", "")).strip()
            if key in {"owner", "data_owner", "technical_owner"} and value:
                owners.append(value)
    normalized["owners"] = sorted(set(owners))

    tags = collect_names(entity.get("globalTags") or entity.get("tags"))
    tags.extend(collect_names(entity.get("glossaryTerms")))
    if isinstance(custom, list):
        for item in custom:
            if not isinstance(item, dict):
                continue
            key = str(item.get("key", "")).lower()
            value = str(item.get("value", "")).lower()
            if key in {"business_critical", "critical"} and value == "true":
                tags.append("critical")
            if key in {"contains_pii", "pii"} and value == "true":
                tags.append("pii")
    normalized["tags"] = sorted(set(tags))
    domain = entity.get("domain")
    if isinstance(domain, dict):
        domain_entity = domain.get("domain", domain)
        if isinstance(domain_entity, dict):
            domain_properties = domain_entity.get("properties", {})
            normalized["domain"] = domain_properties.get("name") or domain_entity.get("urn")
    return normalized


def collect_owners(value: Any) -> list[str]:
    if isinstance(value, list):
        items = value
    elif isinstance(value, dict):
        items = value.get("owners", [])
    else:
        items = []
    owners: list[str] = []
    for item in items:
        if isinstance(item, str):
            owners.append(item)
            continue
        if not isinstance(item, dict):
            continue
        owner = item.get("owner", item)
        if isinstance(owner, str):
            owners.append(owner)
        elif isinstance(owner, dict):
            props = owner.get("properties", {})
            owners.append(
                str(props.get("email") or props.get("displayName") or owner.get("urn") or "")
            )
    return [owner for owner in owners if owner]


def collect_names(value: Any) -> list[str]:
    if isinstance(value, list):
        items = value
    elif isinstance(value, dict):
        items = value.get("tags") or value.get("terms") or []
    else:
        items = []
    names: list[str] = []
    for item in items:
        if isinstance(item, str):
            names.append(item)
            continue
        if not isinstance(item, dict):
            continue
        candidate = item.get("tag") or item.get("term") or item
        if isinstance(candidate, str):
            names.append(candidate)
        elif isinstance(candidate, dict):
            props = candidate.get("properties", {})
            name = props.get("name") or candidate.get("name") or candidate.get("urn")
            if name:
                names.append(str(name))
    return names


def urn_entity_type(urn: str) -> str:
    prefix = "urn:li:"
    if not urn.startswith(prefix):
        return "dataset"
    entity_type = urn[len(prefix) :].split(":", 1)[0]
    aliases = {"mlModel": "mlmodel", "dataFlow": "dataflow", "dataJob": "datajob"}
    return aliases.get(entity_type, entity_type)


def compact_entity(entity: dict[str, Any]) -> dict[str, Any]:
    return {
        key: entity[key]
        for key in ("urn", "name", "type", "platform", "description", "owners", "tags", "domain")
        if key in entity
    }


def extract_text(result: dict[str, Any]) -> str:
    chunks = []
    for item in result.get("content", []):
        if isinstance(item, dict) and item.get("type") == "text":
            chunks.append(str(item.get("text", "")))
    return "\n".join(chunks)


def build_transport(root: Path) -> DataHubTools:
    mode = os.environ.get("RIPPLECHECK_MODE", "fixture").lower()
    if mode == "live":
        command = os.environ.get(
            "DATAHUB_MCP_COMMAND", "uvx mcp-server-datahub@latest"
        )
        return StdioMCPDataHubTools(command)
    if mode != "fixture":
        raise ValueError("RIPPLECHECK_MODE must be 'fixture' or 'live'")
    return FixtureDataHubTools(
        root / "data" / "catalog.json", state_path=root / "data" / "run-state.json"
    )
