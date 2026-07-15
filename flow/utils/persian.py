# Copyright (c) 2026, Frappe Technologies and contributors
# License: MIT. See LICENSE

from __future__ import annotations

import re

ARABIC_TO_PERSIAN = str.maketrans(
	{
		"ك": "ک",
		"ي": "ی",
		"ى": "ی",
		"ة": "ه",
		"ؤ": "و",
		"إ": "ا",
		"أ": "ا",
	}
)
ZERO_WIDTH = re.compile(r"[\u200c\u200d\u200e\u200f]+")
MULTISPACE = re.compile(r"\s+")

PERSIAN_TERM_ALIASES = {
	"کیک": ["cake", "item", "product"],
	"کالا": ["item", "product"],
	"محصول": ["item", "product"],
	"انبار": ["warehouse", "inventory", "stock"],
	"موجودی": ["inventory", "stock", "qty"],
}

DOCTYPE_HINT_ALIASES = {
	"warehouse": ["Warehouse"],
	"inventory": ["Item", "Bin", "Warehouse", "Stock Ledger Entry"],
	"stock": ["Item", "Bin", "Warehouse", "Stock Ledger Entry"],
	"item": ["Item"],
	"product": ["Item"],
	"qty": ["Bin", "Stock Ledger Entry"],
}

FIELD_HINTS = {
	"Item": ["item_name", "item_code", "barcode", "item_group", "description"],
	"Warehouse": ["warehouse_name", "name"],
	"Bin": ["item_code", "warehouse"],
}


def normalize_persian_text(value: str | None) -> str:
	text = (value or "").translate(ARABIC_TO_PERSIAN)
	text = ZERO_WIDTH.sub(" ", text)
	text = MULTISPACE.sub(" ", text).strip()
	return text


def persian_alias_terms(value: str | None) -> list[str]:
	normalized = normalize_persian_text(value).lower()
	if not normalized:
		return []
	terms: list[str] = []
	for token in normalized.split():
		if token not in terms:
			terms.append(token)
		for alias in PERSIAN_TERM_ALIASES.get(token, []):
			if alias not in terms:
				terms.append(alias)
	return terms


def erp_doctype_hints(value: str | None) -> list[str]:
	hints: list[str] = []
	for term in persian_alias_terms(value):
		for doctype in DOCTYPE_HINT_ALIASES.get(term, []):
			if doctype not in hints:
				hints.append(doctype)
	return hints


def erp_record_field_hints(doctype: str) -> list[str]:
	return list(FIELD_HINTS.get(doctype, ["name"]))
