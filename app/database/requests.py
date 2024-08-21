import os
from app.database.models import async_session
from app.database.models import User, Category, Item, Cart
from sqlalchemy import select, update, delete, and_
from datetime import datetime, time, date
import time as tim
import aiofiles
import re

async def set_user(tg_id, chat_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if not user:
            session.add(User(telegram_id=tg_id, telegram_chat_id = chat_id))
            await session.commit()

async def set_initials(tg_id, initial):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            user.initials = initial
            await session.commit()

async def get_user_tg_id(tg_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            return user.telegram_id

async def get_user_chat_id(tg_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            return user.telegram_chat_id

async def get_user_initials(tg_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            return user.initials

async def add_category(category):
    async with async_session() as session:
        cata = await session.scalar(select(Category).filter(Category.category == category))
        if not cata:
            session.add(Category(category = category))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def set_category_id_for_item(category):
    async with async_session() as session:
        print(category)
        cata = await session.scalar(select(Category).filter(Category.category == category))
        if cata:
            session.add(Item(category_id = cata.id))
            await session.commit()
async def set_other_data_about_item(name, description, price):
    async with async_session() as session:
        item = await session.scalar(
            select(Item).filter(
                Item.category_id.isnot(None),
                Item.name.is_(None),
                Item.description.is_(None),
                Item.price.is_(None)
            )
        )
        if item:
            item.name = name
            item.description = description
            item.price = price
        await session.commit()
async def get_items(category):
    async with async_session() as session:
        cata = await session.scalar(select(Category).filter(Category.category == category))
        if cata:
            items = await session.scalars(select(Item).filter(Item.category_id == cata.id))
            return items.all()

async def add_to_cart(tg_id, data):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            cart = await session.scalar(select(Cart).filter(Cart.user_id == user.id))
            if not cart:
                new_data = data.split('.')
                print(new_data)
                items = await session.scalar(select(Item).filter(Item.id == int(new_data[-1])))
                session.add(Cart(user_id=user.id, goods = data, price = items.price))
                await session.commit()
            else:
                last_cart = cart.goods
                new_cart = last_cart + ' ' + data
                cart.goods = new_cart
                new_data = data.split('.')
                items = await session.scalar(select(Item).filter(Item.id == int(new_data[-1])))
                price = int(cart.price)
                new_price = price + int(items.price)
                cart.price = str(new_price)
                await session.commit()

async def get_cart(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            cart = await session.scalar(select(Cart).filter(Cart.user_id == user.id))
            return cart

async def get_item(item_id):
    async with async_session() as session:
        item = await session.scalar(select(Item).filter(Item.id == item_id))
        if item:
            return item

async def del_from_cart(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            cart = await session.scalar(select(Cart).filter(Cart.user_id == user.id))
            goods = cart.goods
            goods = goods.split(' ')
            Flag = False
            new_cart = ''
            new_price = 0
            for item in goods:
                item = item.split('.')
                print('in')
                try:
                    if int(item[-1]) == int(item_id):
                        print('in if')
                        if Flag == False:
                            Flag == True
                            print('in flag')
                            continue
                        else:
                            print('in f else')
                            new_cart += f'{item[0]}.{item[1]}'
                            print(new_cart)
                            items = await session.scalar(select(Item).filter(Item.id == int(item[-1])))
                            new_price += int(items.price)
                    else:
                        print('in else')
                        new_cart += f'{item[0]}.{item[1]}'
                        print(new_cart)
                        items = await session.scalar(select(Item).filter(Item.id == int(item[-1])))
                        new_price += int(items.price)
                except:
                    pass
            print(new_cart, '\n')
            cart.goods = new_cart
            cart.price = str(new_price)
            await session.commit()




