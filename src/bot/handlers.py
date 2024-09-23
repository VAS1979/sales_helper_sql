""" Модуль содержит хэндлеры """

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.processing_requests import Data
from bot.executors import request_processing, repeat_request
from bot.keyboards import start_main, reply_main
from bot.config import HELP

router = Router()


@router.message((F.text == '/start') | (F.text == 'Главное меню'))
async def cmd_start(message: Message):
    """ Обработка команды /start """
    await message.answer("Выберите пункт меню: ",
                         reply_markup=start_main)


@router.message(F.text == 'Помощь')
async def cmd_help(message: Message):
    """ Выводит инструкцию по использованию """
    await message.answer(text=HELP, parse_mode='HTML')
    await message.answer("Выберите пункт меню: ",
                         reply_markup=start_main)


@router.message(F.text == 'Запросить данные')
async def start_query(message: Message, state: FSMContext):
    """ Передает в машину состояния введенные данные """
    await state.set_state(Data.tickers)
    await message.answer("Введите тикеры через запятую:")


@router.message(F.text == 'Новый запрос')
async def tickers_query(message: Message, state: FSMContext):
    """ Передает в машину состояния введенные данные """
    await state.set_state(Data.tickers)
    await message.answer("Введите тикеры через запятую:")


@router.message(F.text == 'Обновить текущий')
async def repeat_query(message: Message):
    """ Передает в машину состояния введенные данные """
    user_id = message.from_user.id
    await message.answer("Введите тикеры через запятую:")
    mess = await repeat_request(user_id)
    await message.answer(mess)


@router.message(Data.tickers)
async def data_saving(message: Message, state: FSMContext):
    """ Передает запрос пользователя бизнес-логике,
    принимает и возвращает пользователю обработанный ответ """
    await state.update_data(tickers=message.text)
    user_id = message.from_user.id
    tickers = message.text
    mess = await request_processing(user_id, tickers)
    await message.answer(mess)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=reply_main)
