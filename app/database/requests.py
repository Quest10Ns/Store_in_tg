import os
from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete, and_
from datetime import datetime, time, date
import time as tim
import aiofiles
import re

async def set_user(tg_id, chat_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if not user:
            session.add(User(telegram_id=tg_id, telegram_chat_id = chat_id))
            await session.commit()

async def set_initials(tg_id, initial):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            user.initials = initial
            await session.commit()

async def get_user_tg_id(tg_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            return user.telegram_id

async def get_user_chat_id(tg_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            return user.telegram_chat_id

async def get_user_initials(tg_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            return user.initials




