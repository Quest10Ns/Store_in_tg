from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

from app.database.requests import get_categories, get_cart, get_item

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

cart_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Заказ', callback_data='oreder'),
     InlineKeyboardButton(text='Удалить из корзины', callback_data='edit_cart')]])

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

async def get_cart_goods(tg_id):
    cart = await get_cart(tg_id)
    goods = cart.goods
    goods = goods.split(' ')
    keyboard = InlineKeyboardBuilder()
    for item in goods:
        item = item.split('.')
        keyboard.add(InlineKeyboardButton(text=f'{(await get_item(item[-1])).name}', callback_data=f'item_{item[-1]}'))
    return keyboard.as_markup()