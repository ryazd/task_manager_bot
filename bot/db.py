from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DB_URL')

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # ID пользователя в Telegram
    text = Column(String(500), nullable=False)  # Текст задачи
    is_done = Column(Boolean, default=False)    # Статус выполнения
    created_at = Column(DateTime, server_default=func.now())  # Дата создания
    dead_line = Column(DateTime, nullable=True) # Дата окончания


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session