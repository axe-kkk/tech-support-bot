from sqlalchemy import BigInteger, Boolean, Column, Integer, String
from db import Base

class SupportChat(Base):
    __tablename__ = "support_chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, index=True, nullable=False)
    topic_id = Column(BigInteger, nullable=True)  # Топик может быть пустым
    username = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)