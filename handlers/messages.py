from handlers.moderation import moderate
from services.intent import detect_intent
from services.responses import build_response, build_keyboard
from services.repository import (
    settings_for,
    record_event,
    record_unknown,
)


def register(bot):
    def on_message(message):
        # يعمل فقط داخل المجموعات
        if message.chat.type not in ("group", "supergroup"):
            return

        # تحميل إعدادات المجموعة
        settings = settings_for(message.chat.id)

        # إذا كان البوت معطلاً في المجموعة
        if not settings.enabled:
            return

        # تشغيل نظام الإشراف
        # إذا تم حذف الرسالة بسبب مخالفة، لا نكمل إلى نظام الأسئلة
        if moderate(bot, message, settings):
            return

        # إذا كانت ميزة الأسئلة الشائعة معطلة
        if not settings.faq_enabled:
            return

        # تجاهل رسائل البوتات الأخرى
        if getattr(message.from_user, "is_bot", False):
            return

        # استخراج النص من الرسالة أو الوصف المصاحب للوسائط
        text = (message.text or message.caption or "").strip()

        if not text:
            return

        # --------------------------------------------------
        # اكتشاف نوع السؤال
        # --------------------------------------------------

        intent = detect_intent(text)

        # إذا لم يتم التعرف على سؤال
        if not intent:
            if (
                settings.capture_unknown
                and (
                    "?" in text
                    or "؟" in text
                    or len(text.split()) >= 4
                )
            ):
                try:
                    record_unknown(
                        message.chat.id,
                        message.from_user.id,
                        text
                    )
                except Exception:
                    pass

            return

        # --------------------------------------------------
        # بناء الإجابة
        # --------------------------------------------------

        response = build_response(intent)

        if not response:
            return

        # --------------------------------------------------
        # بناء زر الرابط المخفي
        # --------------------------------------------------

        try:
            keyboard = build_keyboard(intent)
        except Exception:
            keyboard = None

        # --------------------------------------------------
        # إرسال الإجابة
        # --------------------------------------------------

        try:
            bot.reply_to(
                message,
                response,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )

            # تسجيل نجاح الإجابة
            try:
                record_event(
                    message.chat.id,
                    message.from_user.id,
                    "faq:" + intent
                )
            except Exception:
                pass

        except Exception:
            # تسجيل فشل إرسال الإجابة
            try:
                record_event(
                    message.chat.id,
                    message.from_user.id,
                    "faq_send_failed",
                    intent
                )
            except Exception:
                pass

    # استقبال الرسائل النصية والوسائط التي تحتوي على caption
    bot.register_message_handler(
        on_message,
        content_types=[
            "text",
            "photo",
            "video",
            "document",
            "audio",
            "voice"
        ],
        func=lambda message: bool(
            message.text or message.caption
        )
    )