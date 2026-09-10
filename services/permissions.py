from config import ADMIN_USER_IDS


def is_global_admin(user_id):
    """
    يتحقق هل المستخدم موجود ضمن ADMIN_USER_IDS
    في متغيرات Railway.
    """
    try:
        return int(user_id) in ADMIN_USER_IDS
    except (TypeError, ValueError):
        return False


def is_chat_admin(bot, chat_id, user_id):
    """
    يتحقق هل المستخدم:
    - مالك البوت/أدمن عام
    - مالك المجموعة
    - أدمن في المجموعة

    مهم:
    إذا فشل Telegram API في جلب صلاحية المستخدم،
    نرجع None بدلاً من False حتى لا يتم حذف رسالة
    شخص بسبب خطأ مؤقت في التحقق.
    """

    # أدمن البوت العام
    if is_global_admin(user_id):
        return True

    try:
        member = bot.get_chat_member(chat_id, user_id)

        status = getattr(member, "status", None)

        if status in ("creator", "administrator"):
            return True

        if status in ("member", "restricted", "left", "kicked"):
            return False

        # حالة غير معروفة
        return None

    except Exception:
        return None