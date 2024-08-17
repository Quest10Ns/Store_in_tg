from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from app.database.requests import get_categories

space = ReplyKeyboardRemove()

main_buttuns = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📋Каталог')],
              [KeyboardButton(text='📦Заказы в обработке'), KeyboardButton(text='📦Выполненные заказы')],
              [KeyboardButton(text='Дабаить категорию'), KeyboardButton(text='Добавить в категорию')]], resize_keyboard=True)

edit_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Подтвердить', callback_data='data_is_right'),
     InlineKeyboardButton(text='✏️Изменить', callback_data='editor')]])

edit_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Подтвердить', callback_data='data_is_good'),
     InlineKeyboardButton(text='✏️Изменить', callback_data='data_is_bad')]])

async def get_catas_edit():
    all_cata = await get_categories()
    keyboard = InlineKeyboardBuilder()
    categoties = []
    for category in all_cata:
        if category.category not in categoties:
            categoties.append(category.category)
    for cata in categoties:
        keyboard.add(InlineKeyboardButton(text=f'{cata}', callback_data=f'category_edit_{cata}'))
    return keyboard.as_markup()

async def get_catas():
    all_cata = await get_categories()
    keyboard = InlineKeyboardBuilder()
    categoties = []
    for category in all_cata:
        if category.category not in categoties:
            categoties.append(category.category)
    for cata in categoties:
        keyboard.add(InlineKeyboardButton(text=f'{cata}', callback_data=f'categori_{cata}'))
    return keyboard.as_markup()

edit_item = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Название', callback_data="edit_name"),
                      InlineKeyboardButton(text='Описание', callback_data="edit_desc")],
                     [InlineKeyboardButton(text='Цена', callback_data="edit_price")]])