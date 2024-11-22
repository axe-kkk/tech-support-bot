from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from db import SessionLocal


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with SessionLocal() as session:
            data["session"] = session  # Передаем сессию в контекст
            return await handler(event, data)
