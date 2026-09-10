import logging

from services.moderation import has_link, has_bad_word
from services.permissions import is_chat_admin
from services.repository import record_event


log = logging.getLogger(__name__)


def moderate(bot, message, settings):
    """
    نظام حماية المجموعة.

    القواعد:
    1. الأدمن ومالك المجموعة لا يتم حذف رسائلهم بسبب الروابط.
    2. الأدمن العام الموجود في ADMIN_USER_IDS مستثنى.
    3. روابط الأعضاء العاديين يتم حذفها إذا كان delete_links مفعلاً.
    4. الكلمات المسيئة يتم حذفها إذا كان moderate_bad_words مفعلاً.
    5. إذا تعذر التأكد من صلاحية المستخدم، لا نحذف الرسالة
       احتياطياً لتجنب حذف رسائل الأدمن بالخطأ.
    """

    text = message.text or message.caption or ""

    if not text:
        return False

    # ---------------------------------------------------------
    # التحقق من صلاحيات المستخدم
    # ---------------------------------------------------------

    admin_status = is_chat_admin(
        bot,
        message.chat.id,
        message.from_user.id
    )

    # أدمن مؤكد -> لا تطبق عليه الحماية
    if admin_status is True:
        return False

    # ---------------------------------------------------------
    # إذا تعذر التأكد من صلاحية المستخدم
    # ---------------------------------------------------------
    #
    # لا نحذف الرسالة؛ لأن حذف رسالة أدمن بالخطأ
    # أسوأ من السماح مؤقتاً برسالة مخالفة.
    #
    if admin_status is None:
        log.warning(
            "Could not verify admin status for user %s in chat %s. "
            "Skipping moderation for message %s.",
            message.from_user.id,
            message.chat.id,
            message.message_id,
        )

        record_event(
            message.chat.id,
            message.from_user.id,
            "moderation_permission_check_failed"
        )

        return False

    # ---------------------------------------------------------
    # حذف الروابط
    # ---------------------------------------------------------

    reason = None

    if settings.delete_links and has_link(text):
        reason = "link_deleted"

    # ---------------------------------------------------------
    # حذف الكلمات المسيئة
    # ---------------------------------------------------------

    if (
        not reason
        and settings.moderate_bad_words
        and has_bad_word(text)
    ):
        reason = "bad_word_deleted"

    # لا توجد مخالفة
    if not reason:
        return False

    # ---------------------------------------------------------
    # تنفيذ الحذف
    # ---------------------------------------------------------

    try:
        bot.delete_message(
            message.chat.id,
            message.message_id
        )

        record_event(
            message.chat.id,
            message.from_user.id,
            reason
        )

        log.info(
            "Moderated message %s in chat %s. Reason: %s",
            message.message_id,
            message.chat.id,
            reason,
        )

        return True

    except Exception:
        log.exception(
            "Failed to delete message %s in chat %s",
            message.message_id,
            message.chat.id,
        )

        record_event(
            message.chat.id,
            message.from_user.id,
            "moderation_delete_failed",
            reason
        )

        return False