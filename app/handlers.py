import asyncio
import os
import time as tim
import logging
from datetime import datetime, time, timedelta, date
import re
from aiogram import Bot
from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import app.database.requests as rq
from dotenv import load_dotenv

router = Router()

class Register(StatesGroup):
    initials = State()



@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Добро пожаловать в pankletki. Необходиму пройти простую регистрацию', reply_markup=kb.main)
    await message.answer('Введите ваше ФИО')
    await rq.set_user(message.from_user.id, message.chat.id)
    await state.set_state(Register.initials)
