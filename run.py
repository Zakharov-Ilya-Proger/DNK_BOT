from asyncio import run

from app.bot import dp, bot


async def main():
    await dp.start_polling(
        bot,
        workers=4
    )


if __name__ == '__main__':
    run(main())