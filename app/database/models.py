import os

from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_async_engine(url= os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger)
    initials = mapped_column(String(150))
    telegram_chat_id = mapped_column(BigInteger)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)