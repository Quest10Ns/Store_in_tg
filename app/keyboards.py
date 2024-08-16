from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

from app.database.requests import get_categories

from aiogram.utils.keyboard import InlineKeyboardBuilder

import datetime
space = ReplyKeyboardRemove()

edit_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Подтвердить', callback_data='data_is_right'),
     InlineKeyboardButton(text='✏️Изменить', callback_data='editor')]])

main_buttuns = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📋Каталог')],
              [KeyboardButton(text='🛒Корзина'), KeyboardButton(text='📦Мои заказы')],
              [KeyboardButton(text='ⓘЛичная информация')]], resize_keyboard=True)

edit_main_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅', callback_data='accept'),
     InlineKeyboardButton(text='✏️', callback_data='edit')]])

async def get_catas():
    all_cata = await get_categories()
    keyboard = InlineKeyboardBuilder()
    categoties = []
    for category in all_cata:
        if category.category not in categoties:
            categoties.append(category.category)
    for cata in categoties:
        keyboard.add(InlineKeyboardButton(text=f'{cata}', callback_data=f'category_{cata}'))
    return keyboard.as_markup()