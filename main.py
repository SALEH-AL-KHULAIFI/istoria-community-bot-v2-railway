import logging, time, telebot
from config import BOT_TOKEN, LOG_LEVEL, validate_config
from database import init_database
from handlers import register_handlers

validate_config()
logging.basicConfig(level=getattr(logging,LOG_LEVEL,logging.INFO),format="%(asctime)s %(levelname)s %(name)s: %(message)s")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
init_database()
register_handlers(bot)

def main():
    logging.getLogger(__name__).info("iStoria Community Bot V2 starting")
    while True:
        try:
            bot.infinity_polling(timeout=30, long_polling_timeout=30, allowed_updates=["message"], skip_pending=True)
        except Exception:
            logging.getLogger(__name__).exception("Polling crashed; restarting")
            time.sleep(5)

if __name__ == "__main__":
    main()
