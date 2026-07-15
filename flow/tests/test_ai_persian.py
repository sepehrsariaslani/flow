# Copyright (c) 2026, Frappe Technologies and contributors
# License: MIT. See LICENSE

from frappe.tests import IntegrationTestCase

from flow.utils.persian import (
	erp_doctype_hints,
	erp_record_field_hints,
	normalize_persian_text,
	persian_alias_terms,
)


class TestPersianUtils(IntegrationTestCase):
	def test_normalize_persian_text_unifies_variants(self):
		self.assertEqual(normalize_persian_text("  كيك‌ اوريو  "), "کیک اوریو")

	def test_persian_alias_terms_expands_common_erp_words(self):
		terms = persian_alias_terms("کیک های انبار")
		self.assertIn("کیک", terms)
		self.assertIn("item", terms)
		self.assertIn("inventory", terms)

	def test_erp_doctype_hints_maps_inventory_words(self):
		hints = erp_doctype_hints("موجودی انبار")
		self.assertIn("Item", hints)
		self.assertIn("Bin", hints)
		self.assertIn("Warehouse", hints)

	def test_erp_record_field_hints_for_item_prefers_inventory_fields(self):
		self.assertEqual(
			erp_record_field_hints("Item")[:3],
			["item_name", "item_code", "barcode"],
		)
