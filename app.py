import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from db import init_db
from handlers import setup_routers
from middlewares.db import DbSessionMiddleware

async def main():
    # Инициализация базы данных
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем middleware для передачи сессии
    dp.update.outer_middleware(DbSessionMiddleware())

    # Настраиваем маршруты
    setup_routers(dp)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
