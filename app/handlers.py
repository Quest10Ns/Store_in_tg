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
    if ((await rq.get_user_tg_id(message.from_user.id) is not None) and (
            await rq.get_user_chat_id(message.from_user.id) is not None) and (
            await rq.get_user_initials(message.from_user.id) is not None)):
        await message.answer(
            f'{await rq.get_user_initials(message.from_user.id)}, рады снова Вас приветствовать в PanKletki',
            reply_markup=kb.main_buttuns)
    elif ((await rq.get_user_tg_id(message.from_user.id) is not None) and (
            await rq.get_user_chat_id(message.from_user.id) is not None) and (
                  await rq.get_user_initials(message.from_user.id) is None)):
        await message.answer('Вам необходимо завершить регистрацию')
        await state.set_state(Register.initials)
        await message.answer('Введите ваше ФИО')
    else:
        await message.answer('Добро пожаловать в pankletki. Необходиму пройти простую регистрацию')
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


@router.callback_query(F.data == 'editor')
async def edit_personal_data(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Register.initials)
    await callback.message.answer('Введите новые ФИО', reply_markup=kb.space)


@router.message(F.text == 'ⓘЛичная информация')
async def main_personal_data(message: types.Message):
    if await rq.get_user_initials(message.from_user.id):
        await message.answer(
            f'Ваши данные: \n Количество заказов: in progress \n Сумма выкупа: in progress \n Ваше ФИО: {await rq.get_user_initials(message.from_user.id)}',
            reply_markup=kb.edit_main_buttons)

@router.callback_query(F.data == 'accept')
async def acceppted_personal_data(callback: types.CallbackQuery):
    await callback.answer('Успешно!')
    await callback.message.answer('✅')

@router.callback_query(F.data == 'edit')
async def edit_main_persoanl_data(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Register.initials)
    await callback.message.answer('Введите новые ФИО', reply_markup=kb.space)