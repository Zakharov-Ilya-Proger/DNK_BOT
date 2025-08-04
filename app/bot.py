from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.ai import logger, generate_response
from app.db.db import clear_history
from app.funcs import generate_reply_keyboard, photo_list, generate_inline_key
from app.funcs.answers import answers_dict
from settings import settings

bot = Bot(
    token=settings.TG_BOT_KEY,
    default=DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN,
        link_preview_is_disabled=True,
    ),
)
dp =  Dispatcher()

@dp.message(Command('start'))
async def start(message: Message):
    builder = await generate_reply_keyboard()
    await message.answer(
        '''
            *Привет!* 
        Я бот ДНК, готовый ответить на ваши вопросы по участию в проекте. Ты можешь не только посмотреть уже подготовленные разделы, но и просто задавать мне вопросы текстом в чате
        ''',
        reply_markup=builder
    )


@dp.message(Command('help'))
async def helper(message: Message):
    builder = ReplyKeyboardBuilder()
    button = KeyboardButton(text='/start')
    builder.add(button)
    await message.answer(
        text='''
Если что-то пошло не так, то просто давайте начнем сначала!
        ''',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.message(lambda message: message.text in answers_dict.keys())
async def answer(message: Message):
    logger.info('Z')
    index = list(answers_dict.keys()).index(message.text)
    builder = await generate_reply_keyboard(index)
    if message.text == 'Фильмы':
        await message.answer(
            text=answers_dict[message.text][0],
            reply_markup=await generate_inline_key(
                index=0,
                items=answers_dict[message.text],
                call_pref='film'
            )
        )
        return
    if message.text == 'Инструкции по использованию сайта':
        await message.answer(
            text=answers_dict[message.text][0].text,
            reply_markup=await generate_inline_key(
                index=0,
                items= answers_dict[message.text],
                call_pref='info'
            )
        )
        return

    if message.text == 'У меня проблема':
        await message.answer(
            text=answers_dict[message.text],
            reply_markup=builder,
            parse_mode=None
        )
        return

    await message.answer(
        answers_dict[
            message.text
        ],
        reply_markup=builder
    )


@dp.callback_query(lambda callback: callback.data.split("_")[0] == 'info')
async def info(callback: CallbackQuery):
    index = int(callback.data.split('_')[-1])
    await callback.message.delete()
    data = answers_dict['Инструкции по использованию сайта'][index]

    if data.photo_index is None:
        await callback.message.answer(
            text=data.text,
            reply_markup=await generate_inline_key(
                index=index,
                items=answers_dict['Инструкции по использованию сайта'],
                call_pref='info'
            )
        )
    else:
        await callback.message.answer_photo(
            caption=data.text,
            photo=photo_list[data.photo_index],
            reply_markup=await generate_inline_key(
                index=index,
                items=answers_dict['Инструкции по использованию сайта'],
                call_pref='info'
            )
        )


@dp.callback_query(lambda callback: callback.data.split("_")[0] == 'film')
async def film(callback: CallbackQuery):
    index = int(callback.data.split('_')[-1])
    await callback.message.edit_text(
        text=answers_dict['Фильмы'][index],
        reply_markup=await generate_inline_key(
            index=index,
            items=answers_dict['Фильмы'],
            call_pref='film'
        )
    )


@dp.message(lambda message: message.text == 'Спасибо, ты мне очень помог)')
async def answer(message: Message):
    await message.answer(
        'Всегда пожалуйста, рад был помочь!',
        reply_markup=ReplyKeyboardBuilder().add(KeyboardButton(text='/start')).as_markup(resize_keyboard=True)
    )
    await clear_history(message.from_user.id)


@dp.message()
async def answer_nontypical(message: Message):
    user_answer = await generate_response(message.from_user.id, message.text)
    builder = ReplyKeyboardBuilder()
    keyboard = KeyboardButton(text='Спасибо, ты мне очень помог)')
    builder.add(keyboard)
    await message.answer(user_answer, reply_markup=builder.as_markup(resize_keyboard=True))
