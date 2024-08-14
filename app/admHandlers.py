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
    login = State()
    password = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Это админ панель PANkletki https://t.me/pankletki_bot')
    await message.answer('Введите логин админа')
    await state.set_state(Register.login)

@router.message(Register.login)
async def register_user(message: types.Message, state: FSMContext):
    load_dotenv()
    if message.text == os.getenv('ADMIN_LOGIN'):
        await state.update_data(login=message.text)
        await state.set_state(Register.password)
        await message.answer('ВВедите пароль')
    else:
        await message.answer('Неправильный логин')
        await state.set_state(Register.login)
        await message.answer('Введите корректный логин')

@router.message(Register.password)
async def register_user(message: types.Message, state: FSMContext):
    load_dotenv()
    if message.text == os.getenv('ADMIN_PASSWORD'):
        await state.update_data(password=message.text)
        await state.clear()
        await message.answer('Вход в админ панель выполнен успешно')
    else:
        await message.answer('Неправильный пароль')
        await state.set_state(Register.password)
        await message.answer('Введите корректный пароль')