import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///istoria_community.db").strip()
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://help.istoria.app/ar/").strip()
ADMIN_USER_IDS = {int(x.strip()) for x in os.getenv("ADMIN_USER_IDS", "").split(",") if x.strip().isdigit()}
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def validate_config():
    if not BOT_TOKEN:
        raise RuntimeError("Missing required environment variable: BOT_TOKEN")
