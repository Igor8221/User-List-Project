from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped

from fastapi_users.authentication import CookieTransport

cookie_transport = CookieTransport(cookie_max_age=3600)

DATABASE_URL = "sqlite+aiosqlite:///users.db"

""" создаем свой базовый класс Base, который будет использоваться для создания таблиц """
class Base(DeclarativeBase):
    pass

""" Модель User наследуется от SQLAlchemyBaseUserTableUUID (предоставляется FastAPI Users) и Base. Эта модель представляет таблицу пользователей с UUID в качестве идентификатора """
class User(SQLAlchemyBaseUserTableUUID, Base):
    login: Mapped[str]


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

""" асинхронная функция создает все таблицы в базе данных, определенные в метаданных Base """
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


""" асинхронная функция является генератором, который предоставляет асинхронную сессию для взаимодействия с базой данных """
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

""" асинхронная функция создает объект SQLAlchemyUserDatabase, который используется FastAPI Users для управления пользователями """
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
