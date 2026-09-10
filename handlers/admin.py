from services.permissions import is_chat_admin
from services.repository import settings_for, stats_for

def register(bot):
    def admin(message):
        if message.chat.type not in ("group","supergroup"): return
        if not is_chat_admin(bot,message.chat.id,message.from_user.id): return
        s, a = settings_for(message.chat.id), stats_for(message.chat.id)
        bot.reply_to(message,
            "🛠 لوحة إدارة iStoria\n\n"
            f"الحماية: {'مفعلة' if s.enabled else 'متوقفة'}\n"
            f"حذف الروابط: {'مفعل' if s.delete_links else 'متوقف'}\n"
            f"فلترة الكلمات: {'مفعلة' if s.moderate_bad_words else 'متوقفة'}\n"
            f"FAQ: {'مفعلة' if s.faq_enabled else 'متوقفة'}\n"
            f"الأحداث المسجلة: {a['events']}\n"
            f"الأسئلة غير المعروفة: {a['unknown']}"
        )
    bot.register_message_handler(admin, commands=["admin"])
