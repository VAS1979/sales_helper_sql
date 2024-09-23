""" Модуль содержит клавиатуры """

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

start_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Помощь")],
    [KeyboardButton(text="Запросить данные")]],
                    resize_keyboard=True)

reply_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Новый запрос")],
    [KeyboardButton(text="Обновить текущий")],
    [KeyboardButton(text="Главное меню")],],
                    resize_keyboard=True)
