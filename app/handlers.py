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
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
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


@router.message(F.text == '📋Каталог')
async def check_catalog(message: types.Message):
    keyboard = await kb.get_catas()
    await message.answer('Какую категорию вы хотите посмотреть?', reply_markup=keyboard)

@router.callback_query(F.data.startswith('category_'))
async def show_goods(callback: types.CallbackQuery):
    callback_data = callback.data
    callback_data = callback_data[9::]
    items_list = await rq.get_items(callback_data)
    for item in items_list:
        add_to_cart = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛒Добавить в карзину', callback_data=f'add_to_cart_{item.category_id}_{item.id}')]])
        await callback.message.answer(f'{item.name}\n\n{item.description}\n\nЦена:{item.price} р', reply_markup=add_to_cart)

@router.callback_query(F.data.startswith('add_to_cart_'))
async def add_to_cart(callback: types.CallbackQuery):
    callback_data = callback.data
    print(callback_data)
    callback_data = callback_data.split('_')
    await rq.add_to_cart(callback.from_user.id, f'{callback_data[-2]}.{callback_data[-1]}')
    print(f'{callback_data[-2]}.{callback_data[-1]}')
    await callback.answer('Товар добавлен в корзину')

@router.message(F.text == '🛒Корзина')
async def check_catalog(message: types.Message):
    cart = await rq.get_cart(message.from_user.id)
    cart_string = 'Ваша карзина:\n\n'
    for item in cart.goods.split(' '):
        it = item.split('.')
        item = await rq.get_item(int(it[-1]))
        cart_string += item.name + '\n Цена: ' + item.price + '\n------------------------\n'

    cart_string += 'Общая стоимость корзины: ' + cart.price
    await message.answer(cart_string)


