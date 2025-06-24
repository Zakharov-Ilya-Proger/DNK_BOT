import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.ai.ai_resposes import generate_response
from app.funcs.answers import answers_dict
from app.funcs.build_inline import generate_reply_keyboard
from settings import settings

bot = Bot(
    token=settings.TG_BOT_KEY,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
)
dp =  Dispatcher()

@dp.message(Command('start'))
async def start(message: Message):
    builder = await generate_reply_keyboard()
    await message.answer(
        '''
        <b>Здравствуйте!</b>
    Я бот, который здесь для того, чтобы помочь вам показать ваш фильм на нашем фесте
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


@dp.message(lambda message: ' '.join(message.text.split(' ')[1:]) in answers_dict.keys())
async def answer(message: Message):
    key = ' '.join(message.text.split(' ')[1:])
    index = list(answers_dict.keys()).index(key)
    builder = await generate_reply_keyboard(index)
    await message.answer(
        answers_dict[key],
        reply_markup=builder
    )





@dp.message()
async def answer_nontypical(message: Message):
    user_answer = await generate_response(message.from_user.id, message.text)
    builder = ReplyKeyboardBuilder()
    keyboard = KeyboardButton(text='Спасибо, ты мне очень помог)')
    builder.add(keyboard)
    await message.answer(user_answer, reply_markup=builder.as_markup(resize_keyboard=True))

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())