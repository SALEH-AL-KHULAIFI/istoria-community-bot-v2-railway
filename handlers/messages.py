from handlers.moderation import moderate
from services.intent import detect_intent
from services.responses import build_response
from services.repository import settings_for, record_event, record_unknown

def register(bot):
    def on_message(message):
        if message.chat.type not in ("group", "supergroup"):
            return
        settings = settings_for(message.chat.id)
        if not settings.enabled:
            return
        if moderate(bot, message, settings):
            return
        if not settings.faq_enabled or getattr(message.from_user, "is_bot", False):
            return

        text = (message.text or message.caption or "").strip()
        intent = detect_intent(text)

        if not intent:
            if settings.capture_unknown and ("?" in text or "؟" in text or len(text.split()) >= 4):
                record_unknown(message.chat.id, message.from_user.id, text)
            return

        response = build_response(intent)
        if response:
            try:
                bot.reply_to(message, response, disable_web_page_preview=True)
                record_event(message.chat.id, message.from_user.id, "faq:" + intent)
            except Exception:
                record_event(message.chat.id, message.from_user.id, "faq_send_failed", intent)

    bot.register_message_handler(
        on_message,
        content_types=["text", "photo", "video", "document", "audio", "voice"],
        func=lambda message: bool(message.text or message.caption)
    )
