from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Преподаватель'), KeyboardButton(text = 'Студент')]],
                           resize_keyboard=True, input_field_placeholder='Выберите пункт меню...')

edit_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Подтвердить', callback_data='data_is_right'),
     InlineKeyboardButton(text='✏️Изменить', callback_data='editor')]])

main_buttuns_for_student = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📋Каталог')],
              [KeyboardButton(text='🛒Корзина'), KeyboardButton(text='❤️Избранное')],
              [KeyboardButton(text='📦Мои заказы')]], resize_keyboard=True)
