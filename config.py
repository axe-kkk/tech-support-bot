import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///support_bot.db")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID", "YOUR_GROUP_CHAT_ID")  # ID группы специалистов