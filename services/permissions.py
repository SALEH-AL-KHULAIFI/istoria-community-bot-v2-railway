from config import ADMIN_USER_IDS

def is_global_admin(user_id): return user_id in ADMIN_USER_IDS

def is_chat_admin(bot, chat_id, user_id):
    if is_global_admin(user_id): return True
    try: return bot.get_chat_member(chat_id,user_id).status in ("administrator","creator")
    except Exception: return False
