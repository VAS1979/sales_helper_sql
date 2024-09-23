""" Обработка запроса бота и формирование итоговых данных """
import json

from aiogram.fsm.state import StatesGroup, State


class Data(StatesGroup):
    """ Класс модель для заполнения
    данных пользователя """
    tickers = State()


async def input_validation(input_string):
    """ Провереряет корректность ввода пользователем
     и возвращает только правильно введенные тикеры """
    with open("db/parsed_data.json", encoding="utf-8") as f:
        parsed_data = json.load(f)

    finished_result = ''
    for ticker in input_string.upper().split(", "):
        for pair in parsed_data["data"]:
            if pair[0] == ticker:
                finished_result += pair[0] + ' '
    return finished_result[0:-1]


async def processing_sql_data(user_data):
    """ Считывает данные из sql на основании запроса
    пользователя, обрабатывает и сохраняет результат """
    with open("db/parsed_data.json", encoding="utf-8") as f:
        parsed_data = json.load(f)

    finished_result = ''
    for ticker in user_data.upper().split(", "):
        for pair in parsed_data["data"]:
            if pair[0] == ticker:
                st = str(pair).replace("'", '')[1:-1].replace(',', ':') + ", "
                finished_result += st
    final_string = finished_result[0:-2]

    data = {"datetime": parsed_data["datetime"],
            "stock_quotes": final_string}

    return data


async def convert_tuple_to_string(data):
    """ Конвертирует кортеж в строку """
    data = str(data)[2:-3]

    final_string = ""
    for i in data:
        if i == ' ':
            i = ', '
        final_string += i
    return final_string


async def create_finish_string(data):
    """ Формирует итоговую строку для бота """
    datetime = data[0]
    quotes = data[1]

    quotes = quotes.replace(':', ' '*7)
    quotes = quotes.replace(', ', '\n')

    final_string = f"Данные получены с MOEX:   {datetime}\n\n{quotes}"

    return final_string
