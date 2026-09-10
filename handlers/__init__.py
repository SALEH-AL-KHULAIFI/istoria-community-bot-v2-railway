from handlers.admin import register as register_admin
from handlers.messages import register as register_messages


def register_handlers(bot):
    register_admin(bot)
    register_messages(bot)