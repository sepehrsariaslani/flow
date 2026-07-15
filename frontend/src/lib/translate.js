// Thin wrapper over the desk's global translator so components can stay
// translatable without depending on it being present (e.g. in isolation).
const FA_MESSAGES = {
	Flow: "فلو",
	"Toggle Flow panel": "باز و بسته کردن پنل فلو",
	"Flow failed to load. Refresh the page to retry.": "بارگذاری فلو ناموفق بود. صفحه را تازه‌سازی کنید و دوباره تلاش کنید.",
	"Thinking…": "در حال فکر کردن…",
	"Response interrupted": "پاسخ متوقف شد",
	"Search…": "جستجو…",
	"Searching…": "در حال جستجو…",
	"Search sessions…": "جستجوی نشست‌ها…",
	"Previous sessions": "نشست‌های قبلی",
	"Loading…": "در حال بارگذاری…",
	"Setup required…": "نیاز به تنظیم اولیه…",
	"Ask {0}…": "از {0} بپرس…",
	"Default": "پیش‌فرض",
	"Agent": "عامل",
	"Model": "مدل",
	"Send": "ارسال",
	"Stop": "توقف",
	"Cancel": "لغو",
	"Remove": "حذف",
	"Attach file": "پیوست فایل",
	"Uploading…": "در حال بارگذاری فایل…",
	"Failed": "ناموفق",
	"Couldn't attach file": "پیوست فایل ناموفق بود",
	"New chat": "گفت‌وگوی جدید",
	"Full screen": "تمام‌صفحه",
	"Exit full screen": "خروج از تمام‌صفحه",
	"Close (Ctrl+I)": "بستن (Ctrl+I)",
	"Finish setup to start": "برای شروع، تنظیمات را کامل کنید",
	"The assistant needs a few things configured first:": "دستیار قبل از شروع به چند تنظیم نیاز دارد:",
	"Create and enable a Flow Model with your provider credentials.":
		"یک مدل Flow بسازید و با اطلاعات ارائه‌دهنده‌تان فعالش کنید.",
	"Ask about your data, draft records, or run a task.": "درباره داده‌هایتان بپرسید، پیش‌نویس رکورد بسازید یا یک کار را اجرا کنید.",
	"Show more": "نمایش بیشتر",
	"Show less": "نمایش کمتر",
	"Show {0} more": "نمایش {0} مورد بیشتر",
	"Show {0} more lines": "نمایش {0} خط بیشتر",
	"+{0} more": "+{0} مورد دیگر",
	"Record {0}": "رکورد {0}",
	"Other…": "سایر…",
	"Describe what you want instead…": "بگویید به‌جای آن چه می‌خواهید…",
	"Searching Knowledge": "در حال جستجوی دانش",
	"Finding relevant DocTypes": "در حال پیدا کردن داک‌تایپ‌های مرتبط",
	"Reading DocType Meta": "در حال خواندن متادیتای داک‌تایپ",
	"Reading DocType Records": "در حال خواندن رکوردهای داک‌تایپ",
	"Searching Records": "در حال جستجوی رکوردها",
	"Executing": "در حال اجرا",
	"Creating Records": "در حال ساختن رکوردها",
	"Updating Records": "در حال به‌روزرسانی رکوردها",
	"Deleting Records": "در حال حذف رکوردها",
	"Running Document Actions": "در حال اجرای عملیات سند",
	"Yes": "بله",
	"No": "خیر",
	"Denied": "رد شد",
	"Changes requested": "درخواست تغییر ثبت شد",
	"Ran {0} steps": "{0} مرحله اجرا شد",
	"Run Python code": "اجرای کد پایتون",
	"records": "رکوردها",
	"No matches": "موردی پیدا نشد",
	"No matching sessions": "نشست منطبقی پیدا نشد",
	"No recent sessions": "نشست اخیر وجود ندارد",
};

function formatMessage(message, args) {
	if (!args?.length) return message;
	return args.reduce((result, value, index) => result.replaceAll(`{${index}}`, String(value)), message);
}

function isPersianDesk() {
	if (typeof window === "undefined") return false;
	const lang = window.frappe?.boot?.lang || document?.documentElement?.lang || "";
	return String(lang).toLowerCase().startsWith("fa");
}

export function __(message, args) {
	if (typeof window !== "undefined" && typeof window.__ === "function") {
		const translated = window.__(message, args);
		if (translated && translated !== message) return translated;
	}
	if (isPersianDesk() && FA_MESSAGES[message]) {
		return formatMessage(FA_MESSAGES[message], args);
	}
	return formatMessage(message, args);
}
