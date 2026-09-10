from telebot import types

from services.knowledge import answer_for


def build_response(intent):
    """
    يبني نص الإجابة فقط.

    الروابط لا تظهر داخل نص الرسالة،
    وإنما يتم وضعها داخل زر Inline أسفل الرسالة.
    """

    item = answer_for(intent)

    if not item:
        return None

    return item.get("answer")


def build_keyboard(intent):
    """
    ينشئ زر Inline للرابط المرتبط بالإجابة.

    الرابط نفسه لا يظهر للمستخدم داخل نص الرسالة.
    """

    item = answer_for(intent)

    if not item:
        return None

    source = item.get("source")

    if not source:
        return None

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    button_text = "📖 تفاصيل أكثر"

    if intent == "support":
        button_text = "🆘 الدعم الرسمي"

    elif intent == "subscribe":
        button_text = "💳 طريقة الاشتراك"

    elif intent == "pricing_redirect":
        button_text = "💰 تفاصيل الاشتراك"

    elif intent == "family_subscription":
        button_text = "👨‍👩‍👧‍👦 تفاصيل الاشتراك العائلي"

    elif intent == "free_trial":
        button_text = "🎁 تفاصيل التجربة المجانية"

    elif intent == "cancel_subscription":
        button_text = "⚙️ إدارة وإلغاء الاشتراك"

    elif intent == "refund":
        button_text = "💳 معلومات الاسترداد"

    elif intent == "premium":
        button_text = "⭐ تفاصيل Premium"

    elif intent == "chat_istro":
        button_text = "💬 تفاصيل Chat with iStro"

    elif intent == "password_reset":
        button_text = "🔐 استعادة كلمة المرور"

    elif intent == "delete_account":
        button_text = "🗑️ تفاصيل حذف الحساب"

    elif intent == "device_compatibility":
        button_text = "📱 متطلبات الأجهزة"

    elif intent == "what_is_istoria":
        button_text = "📖 تعرف على iStoria"

    elif intent == "legend_challenge":
        button_text = "اضغط هنا"

    keyboard.add(
        types.InlineKeyboardButton(
            text=button_text,
            url=source
        )
    )

    return keyboard