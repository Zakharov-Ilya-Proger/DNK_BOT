from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

from app.funcs.answers import answers_dict

buttons_list_old = (
    KeyboardButton(
        text='1. Вступите в чат',
        url='https://t.me/dnk_csff'
    ),
    KeyboardButton(
        text='2. Выберите фильмы',
        callback_data='step_0'
    ),
    KeyboardButton(
        text='3. Регистрация',
        callback_data='step_1'
    ),
    KeyboardButton(
        text='4. Расписание',
        callback_data='step_2'
    ),
    KeyboardButton(
        text='5. Найдите эксперта',
        callback_data='step_3'
    ),
    KeyboardButton(
        text='6. Соцсети',
        callback_data='step_4'
    ),
    KeyboardButton(
        text='7. Аудитория',
        callback_data='step_5'
    ),
    KeyboardButton(
        text='8. Показ',
        callback_data='step_6'
    ),
    KeyboardButton(
        text='9. Отчет по мероприятию',
        callback_data='step_7'
    ),
    KeyboardButton(
        text='10. Общий отчет',
        callback_data='step_8'
    )
)


buttons_list_new = list((
    KeyboardButton(
        text=text,
        callback_data=f'step_{index}'
    )
    for index, text in enumerate(answers_dict)
))


async def generate_reply_keyboard(exclude_index: int = None):
    builder = ReplyKeyboardBuilder()

    if exclude_index is None:
        buttons_to_add = buttons_list_new
    else:
        buttons_to_add = buttons_list_new[:exclude_index] + buttons_list_new[exclude_index + 1:]

    for button in buttons_to_add:
        builder.add(button)

    builder.adjust(1, repeat=True)
    return builder.as_markup(resize_keyboard=True)