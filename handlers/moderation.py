import logging
from services.moderation import has_link, has_bad_word
from services.permissions import is_chat_admin
from services.repository import record_event
log = logging.getLogger(__name__)

def moderate(bot, message, settings):
    text = message.text or message.caption or ""
    if not text or is_chat_admin(bot,message.chat.id,message.from_user.id): return False
    reason = "link_deleted" if settings.delete_links and has_link(text) else None
    if not reason and settings.moderate_bad_words and has_bad_word(text): reason = "bad_word_deleted"
    if not reason: return False
    try:
        bot.delete_message(message.chat.id,message.message_id)
        record_event(message.chat.id,message.from_user.id,reason)
        return True
    except Exception:
        log.exception("Failed to delete message %s",message.message_id)
        record_event(message.chat.id,message.from_user.id,"moderation_delete_failed",reason)
        return False
