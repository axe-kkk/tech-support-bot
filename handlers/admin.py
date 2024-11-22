from aiogram import Router, F, Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_user_by_topic

router = Router()


@router.message(F.chat.type.in_({"group", "supergroup"}), F.text.startswith("/close"))
async def close_request_handler(message: Message, bot: Bot, session: AsyncSession):
    # Убедимся, что команда используется как ответ на сообщение
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть использована как ответ на сообщение.")
        return

    # Получаем topic_id из reply_to_message
    topic_id = message.reply_to_message.message_id
    print(f"Закрытие вопроса с topic_id={topic_id}")

    # Находим пользователя по topic_id
    user = await get_user_by_topic(session, topic_id)
    if not user:
        await message.reply("Не удалось найти пользователя для закрытия запроса.")
        return

    # Отправляем шаблонное сообщение пользователю
    try:
        await bot.send_message(
            chat_id=user.user_id,
            text=(
                "Были рады помочь вам с вашим вопросом. "
                "В случае возникновения других вопросов, наши специалисты с радостью ответят как можно скорее."
            ),
        )
        print(f"Шаблонное сообщение отправлено user_id={user.user_id}")
        await message.reply("Вопрос успешно закрыт.")
    except Exception as e:
        print(f"Ошибка отправки шаблонного сообщения: {e}")
        await message.reply("Произошла ошибка при закрытии вопроса.")


@router.message(F.chat.type.in_({"group", "supergroup"}))
async def admin_response_handler(message: Message, bot: Bot, session: AsyncSession):
    if not message.reply_to_message:
        print("Сообщение не является ответом")
        return

    # Получаем ID сообщения, на которое ответил специалист
    topic_id = message.reply_to_message.message_id
    print(f"Получен topic_id={topic_id} для ответа")

    # Получаем пользователя по topic_id
    user = await get_user_by_topic(session, topic_id)
    if not user:
        print(f"Пользователь не найден для topic_id={topic_id}")
        await message.reply("Не удалось найти пользователя для ответа.")
        return

    # Отправляем сообщение пользователю
    try:
        await bot.send_message(
            chat_id=user.user_id,
            text=f"Ответ от специалиста:\n{message.text}"
        )
        print(f"Ответ отправлен user_id={user.user_id}")
        await message.reply("Ответ успешно отправлен пользователю.")
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        await message.reply(f"Ошибка при отправке сообщения пользователю: {e}")
