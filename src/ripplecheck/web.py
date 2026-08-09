"""Tiny HTTP API and static-file server for the deployable demo."""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import threading
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from .agent import RipplecheckAgent
from .evidence_pack import build_evidence_pack
from .scenarios import SCENARIOS
from .transport import DataHubTools


MAX_BODY_BYTES = 32_768


def create_handler(root: Path, tools: DataHubTools) -> type[BaseHTTPRequestHandler]:
    public = (root / "public").resolve()
    agent = RipplecheckAgent(tools)
    assessments: dict[str, dict[str, Any]] = {}
    assessment_lock = threading.Lock()

    class DemoHandler(BaseHTTPRequestHandler):
        server_version = "Ripplecheck/2.0"

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path
            if path == "/health":
                self._json(HTTPStatus.OK, {"status": "ok", "mode": "offline-ready"})
                return
            if path == "/api/scenarios":
                self._json(HTTPStatus.OK, {"scenarios": SCENARIOS})
                return
            if path.startswith("/api/evidence-pack/"):
                run_id = path.rsplit("/", 1)[-1]
                with assessment_lock:
                    assessment = assessments.get(run_id)
                if assessment is None:
                    change = (parse_qs(parsed.query).get("change") or [""])[0]
                    if change:
                        candidate = agent.assess(change, writeback=False)
                        if candidate["run_id"] == run_id:
                            assessment = candidate
                if assessment is None:
                    self._json(HTTPStatus.NOT_FOUND, {"error": "Run not found. Compile it first."})
                    return
                self._download_pack(assessment)
                return
            self._static(path)

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path != "/api/analyze":
                self._json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size <= 0 or size > MAX_BODY_BYTES:
                    raise ValueError("Request body must be between 1 byte and 32 KB.")
                payload = json.loads(self.rfile.read(size))
                if not isinstance(payload, dict):
                    raise ValueError("Request body must be a JSON object.")
                change = payload.get("change", "")
                if not isinstance(change, str):
                    raise ValueError("change must be a string.")
                result = agent.assess(change, writeback=bool(payload.get("writeback", True)))
                with assessment_lock:
                    assessments[result["run_id"]] = result
                self._json(HTTPStatus.OK, result)
            except (json.JSONDecodeError, ValueError) as exc:
                self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            except RuntimeError as exc:
                self._json(HTTPStatus.BAD_GATEWAY, {"error": str(exc)})

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _static(self, request_path: str) -> None:
            relative = unquote(request_path).lstrip("/") or "index.html"
            candidate = (public / relative).resolve()
            if public not in candidate.parents and candidate != public:
                self._json(HTTPStatus.FORBIDDEN, {"error": "Forbidden"})
                return
            if not candidate.is_file():
                candidate = public / "index.html"
            content = candidate.read_bytes()
            mime = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", f"{mime}; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache" if candidate.name == "index.html" else "public, max-age=3600")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'")
            self.end_headers()
            self.wfile.write(content)

        def _download_pack(self, assessment: dict[str, Any]) -> None:
            body = build_evidence_pack(assessment)
            filename = f"ripplecheck-{assessment['change_capsule']['capsule_id'].lower()}.zip"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

    return DemoHandler


def run_web(root: Path, tools: DataHubTools, host: str, port: int) -> None:
    server = ThreadingHTTPServer((host, port), create_handler(root, tools))
    print(f"Ripplecheck demo listening on http://{host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
