""" Точка входа """
import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import TOKEN
from bot.handlers import router
from bot.models import create_db_tables
from parsers.parser import data_parsing

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    """ Функция запуска приложения """
    asyncio.create_task(create_db_tables())
    asyncio.create_task(data_parsing())
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # при деплое отключить
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
