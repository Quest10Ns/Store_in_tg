import os

from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Text, Integer, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger)
    initials = mapped_column(String(300))
    telegram_chat_id = mapped_column(BigInteger)


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    category = mapped_column(String(150), nullable=True)


class Item(Base):
    __tablename__ = 'goods'
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id = mapped_column(ForeignKey('categories.id'))
    name = mapped_column(String(200), nullable=True)
    description = mapped_column(Text, nullable=True)
    price = mapped_column(String(200), nullable=True)

class Cart(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('users.id'))
    goods = mapped_column(String(300), nullable=True)
    price = mapped_column(String(200), nullable=True)
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
