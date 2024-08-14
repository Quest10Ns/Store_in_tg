from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

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
