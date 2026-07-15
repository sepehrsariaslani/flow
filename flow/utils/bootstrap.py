from __future__ import annotations

import frappe


def ensure_flow_module_map() -> None:
	"""Ensure Frappe's in-process module map knows about the Flow module.

	Some fresh processes can start with a stale or incomplete installed_app_modules cache,
	which leaves `frappe.local.module_app["flow"]` unset and breaks Flow DocType imports.
	Repair the local maps eagerly from modules.txt so Flow doctypes resolve reliably.
	"""
	module_app = getattr(frappe.local, "module_app", None)
	app_modules = getattr(frappe.local, "app_modules", None)
	if module_app and module_app.get("flow") == "flow":
		return

	frappe.setup_module_map(include_all_apps=False)
	module_app = getattr(frappe.local, "module_app", None)
	app_modules = getattr(frappe.local, "app_modules", None)
	if not isinstance(module_app, dict):
		module_app = frappe.local.module_app = {}
	if not isinstance(app_modules, dict):
		app_modules = frappe.local.app_modules = {}

	flow_modules = [frappe.scrub(module) for module in frappe.get_module_list("flow")]
	if not flow_modules:
		return

	app_modules["flow"] = flow_modules
	for module in flow_modules:
		module_app[module] = "flow"
