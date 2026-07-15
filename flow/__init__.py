from __future__ import annotations

__version__ = "0.0.1"

try:
	import frappe
except Exception:  # pragma: no cover - package import should stay cheap outside Frappe
	frappe = None
else:
	module_app = getattr(getattr(frappe, "local", None), "module_app", None)
	if isinstance(module_app, dict):
		module_app.setdefault("flow", "flow")

from flow.lib.agent import Agent, RunResult
from flow.lib.model import ChatResponse, Model, ToolCall
from flow.lib.tool import Tool, build_schema, tool

__all__ = [
	"Agent",
	"ChatResponse",
	"Model",
	"RunResult",
	"Tool",
	"ToolCall",
	"build_schema",
	"tool",
]
