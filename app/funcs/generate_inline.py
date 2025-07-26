from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.model import CallbackListElement


async def generate_inline_key(index: int, items: list[CallbackListElement], call_pref):

    builder = InlineKeyboardBuilder()

    if index == 0:
        return builder.add(
            InlineKeyboardButton(text='Дальше→', callback_data=f'{call_pref}_{index + 1}')
        ).as_markup(
            resize_keyboard=True
        )
    elif index == len(items) - 1:
        return builder.add(
            InlineKeyboardButton(text='←Назад', callback_data=f'{call_pref}_{index - 1}')
        ).as_markup(
            resize_keyboard=True
        )
    else:
        return builder.add(
            InlineKeyboardButton(text='←Назад', callback_data=f'{call_pref}_{index - 1}')
        ).add(
            InlineKeyboardButton(text='Дальше→', callback_data=f'{call_pref}_{index + 1}')
        ).as_markup(
            resize_keyboard=True
        )
