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
        user = await session.scalar(select(User.telegram_id == tg_id))
        if not user:
            session.add(User(telegram_id=tg_id, telegram_chat_id = chat_id))
            await session.commit()