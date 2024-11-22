from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import SupportChat


async def get_user_by_topic(session: AsyncSession, topic_id: int):
    stmt = select(SupportChat).where(SupportChat.topic_id == topic_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        print(f"Нет записи в базе данных для topic_id={topic_id}")
    else:
        print(f"Найден user_id={user.user_id} для topic_id={topic_id}")

    return user



async def create_support_chat(session: AsyncSession, user_id: int, username: str, topic_id: int):
    # Проверяем, существует ли пользователь в базе
    stmt = select(SupportChat).where(SupportChat.user_id == user_id)
    result = await session.execute(stmt)
    existing_chat = result.scalar_one_or_none()

    if existing_chat:
        # Обновляем topic_id, если он изменился
        if existing_chat.topic_id != topic_id:
            existing_chat.topic_id = topic_id
            await session.commit()  # Фиксируем изменения
            print(f"Обновлена связь: user_id={user_id}, topic_id={topic_id}")
        return

    # Если пользователь новый, создаем запись
    chat = SupportChat(user_id=user_id, username=username, topic_id=topic_id)
    session.add(chat)
    await session.commit()  # Сохраняем изменения
    print(f"Создана новая запись: user_id={user_id}, topic_id={topic_id}")
