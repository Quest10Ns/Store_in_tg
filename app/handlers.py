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

@router.message(Register.initials)
async def register_user(message: types.Message, state: FSMContext):
    await state.update_data(initials=message.text)
    await rq.set_initials(message.from_user.id, message.text)
    data = await state.get_data()
    await message.answer(
        f'Ваше ФИО: {data["initials"]}', reply_markup=kb.edit_button)
    await state.clear()

@router.callback_query(F.data == 'data_is_right')
async def accepst_initials(callback: types.CallbackQuery):
    await callback.message.answer('Отлично, регистрация успешно пройдена!',
                                      reply_markup=kb.main_buttuns)
    await callback.answer()