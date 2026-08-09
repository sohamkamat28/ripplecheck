"""Vercel Python Function adapter for Ripplecheck's dependency-free web handler."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ripplecheck.transport import FixtureDataHubTools  # noqa: E402
from ripplecheck.web import create_handler  # noqa: E402


TOOLS = FixtureDataHubTools(ROOT / "data" / "catalog.json")
BaseHandler = create_handler(ROOT, TOOLS)


class handler(BaseHandler):
    """Expose the shared handler as a Vercel Python Function."""
