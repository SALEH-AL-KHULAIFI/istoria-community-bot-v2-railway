from config import SUPPORT_URL
from services.knowledge import answer_for

def build_response(intent):
    if intent == "pricing_redirect":
        return "بالنسبة للأسعار والخصومات وتكلفة الاشتراك، هذا البوت لا يقدّم معلومات سعرية.\nللمعلومات الرسمية والحالية راجع دعم iStoria الرسمي:\n" + SUPPORT_URL
    item = answer_for(intent)
    return item["answer"] if item else None
