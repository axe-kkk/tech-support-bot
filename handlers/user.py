from aiogram import Router, Bot, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from config import GROUP_CHAT_ID
from utils import create_support_chat

router = Router()


@router.message(F.chat.type == "private", F.text == "/start")
async def start_handler(message: Message, session: AsyncSession):

    await message.answer(
        "Добро пожаловать в техподдержку! "
        "Напишите ваш вопрос, и наши специалисты ответят как можно скорее."
    )


@router.message(F.chat.type == "private", ~F.text.startswith("/"))
async def user_message_handler(message: Message, bot: Bot, session: AsyncSession):
    # Отправляем сообщение в группу специалистов
    topic_message = await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=f"Вопрос от {message.from_user.full_name} (@{message.from_user.username}):\n{message.text}",
    )

    # Сохраняем связь user_id ↔ topic_id
    await create_support_chat(
        session=session,
        user_id=message.from_user.id,
        username=message.from_user.username,
        topic_id=topic_message.message_id
    )

    # Отладочный вывод
    print(f"Связь для user_id={message.from_user.id} обновлена на topic_id={topic_message.message_id}")

    await message.answer("Ваш вопрос отправлен специалистам. Ожидайте ответа!")


