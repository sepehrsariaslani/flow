import test from "node:test";
import assert from "node:assert/strict";

import { __ } from "./translate.js";

test("returns persian Flow-local labels when desk language is fa", () => {
	global.window = { frappe: { boot: { lang: "fa" } } };
	assert.equal(__("Thinking…"), "در حال فکر کردن…");
	assert.equal(__("Search…"), "جستجو…");
	assert.equal(__("Searching Records"), "در حال جستجوی رکوردها");
	assert.equal(__("Show {0} more", [3]), "نمایش 3 مورد بیشتر");
	delete global.window;
});

test("prefers desk translations when provided", () => {
	global.window = {
		frappe: { boot: { lang: "fa" } },
		__: (message) => (message === "Send" ? "بفرست" : message),
	};
	assert.equal(__("Send"), "بفرست");
	delete global.window;
});
