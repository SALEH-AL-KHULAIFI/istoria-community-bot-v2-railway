# iStoria Community Bot V2 — Railway

نسخة مخصصة للنشر على Railway كـ Worker باستخدام Telegram Long Polling.

Start Command:
`python main.py`

متغيرات البيئة:
- BOT_TOKEN: سري ومطلوب
- DATABASE_URL: اختياري، SQLite للاختبار وPostgreSQL للإنتاج
- SUPPORT_URL=https://help.istoria.app/ar/
- ADMIN_USER_IDS: Telegram IDs مفصولة بفواصل
- LOG_LEVEL=INFO

لا تستخدم Webhook أو Vercel مع هذه النسخة. تأكد من تعطيل Privacy Mode ومنح البوت صلاحية حذف الرسائل في المجموعة.
