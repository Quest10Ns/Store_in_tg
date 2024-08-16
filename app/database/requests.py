import os
from app.database.models import async_session
from app.database.models import User, Category, Item
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

async def add_category(category):
    async with async_session() as session:
        cata = await session.scalar(select(Category).filter(Category.category == category))
        if not cata:
            session.add(Category(category = category))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def set_category_id_for_item(category):
    async with async_session() as session:
        cata = await session.scalar(select(Category).filter(Category.category == category))
        if cata:
            session.add(Item(category_id = cata.id))
async def set_other_data_about_item(name, description, price):
    async with async_session() as session:
        item = await session.scalar(
            select(Item).filter(
                Item.category_id.isnot(None),
                Item.name.is_(None),
                Item.description.is_(None),
                Item.price.is_(None)
            )
        )
        if item:
            item.name = name
            item.description = description
            item.price = price
        session.commit()
