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
import app.admKeyboards as kb
import app.database.requests as rq
from dotenv import load_dotenv

router2 = Router()


class Register(StatesGroup):
    login = State()
    password = State()


class setCategory(StatesGroup):
    category = State()


class setItem(StatesGroup):
    name = State()
    description = State()
    price = State()


@router2.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Это админ панель PANkletki https://t.me/pankletki_bot')
    await message.answer('Введите логин админа')
    await state.set_state(Register.login)


@router2.message(Register.login)
async def register_user(message: types.Message, state: FSMContext):
    load_dotenv()
    if message.text == os.getenv('ADMIN_LOGIN'):
        await state.update_data(login=message.text)
        await state.set_state(Register.password)
        await message.answer('ВВедите пароль')
    else:
        await message.answer('Неправильный логин')
        await state.set_state(Register.login)
        await message.answer('Введите правильный логин')


@router2.message(Register.password)
async def register_user(message: types.Message, state: FSMContext):
    load_dotenv()
    if message.text == os.getenv('ADMIN_PASSWORD'):
        await state.update_data(password=message.text)
        await state.clear()
        await message.answer('Вход в админ панель выполнен успешно', reply_markup=kb.main_buttuns)
    else:
        await message.answer('Неправильный пароль')
        await state.set_state(Register.password)
        await message.answer('Введите правильный пароль')


@router2.message(F.text == 'Дабаить категорию')
async def add_categoty(message: types.Message, state: FSMContext):
    await message.answer('ВВедите категорию')
    await state.set_state(setCategory.category)


@router2.message(setCategory.category)
async def set_category(message: types.Message, state: FSMContext):
    await state.update_data(categoty=message.text)
    await rq.add_category(message.text)
    data = await state.get_data()
    await message.answer(
        f'Категория: {data["categoty"]}', reply_markup=kb.edit_button)
    await state.clear()


@router2.callback_query(F.data == 'data_is_right')
async def accepst_initials(callback: types.CallbackQuery):
    await callback.message.answer('Категория успешно добавлена',
                                  reply_markup=kb.main_buttuns)
    await callback.answer()


@router2.callback_query(F.data == 'editor')
async def edit_personal_data(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(setCategory.category)
    await callback.message.answer('Введите категорию', reply_markup=kb.space)


@router2.message(F.text == '📋Каталог')
async def check_catalog(message: types.Message):
    keyboard = await kb.get_catas()
    await message.answer('Какую категорию вы хотите посмотреть?', reply_markup=keyboard)

@router2.callback_query(F.data.startswith('categori_'))
async def show_goods(callback: types.CallbackQuery):
    callback_data = callback.data
    callback_data = callback_data[9::]
    items_list = await rq.get_items(callback_data)
    for item in items_list:
        await callback.message.answer(f'{item.name}\n\n{item.description}\n\nЦена:{item.price} р')

@router2.message(F.text == 'Добавить в категорию')
async def add_categoty(message: types.Message, state: FSMContext):
    keyboard = await kb.get_catas_edit()
    await message.answer('Выберите категорию', reply_markup=keyboard)


@router2.callback_query(F.data.startswith('category_edit_'))
async def add_item(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data
    callback_data = callback_data[14::]
    await rq.set_category_id_for_item(callback_data)
    await state.set_state(setItem.name)
    await callback.message.answer('Введите название')

@router2.message(setItem.name)
async def set_item_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(setItem.description)
    await message.answer('Введите описание')

@router2.message(setItem.description)
async def set_item_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(setItem.price)
    await message.answer('Введите цену')

@router2.message(setItem.price)
async def set_item_description(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await rq.set_other_data_about_item(data["name"], data["description"], data["price"])
    await message.answer(
        f'Назввание: {data["name"]}\nОписание: {data["description"]}\nЦена: {data["price"]}', reply_markup=kb.main_buttuns)
    await state.clear()
