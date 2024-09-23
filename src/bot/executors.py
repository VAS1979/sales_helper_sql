""" Модуль содержит функции, содержащие цепочку вызовов всех функций """
from bot.models import (insert_userdata, writing_finished_data,
                        returning_finished_data)


async def request_processing(user_id, tickers):
    """ Обрабатывает последовательно цепочку
    действий от запроса пользователя до возрата итога """

    await insert_userdata(user_id, tickers)
    await writing_finished_data(user_id)
    mess = await returning_finished_data(user_id)

    return mess


async def repeat_request(user_id):
    """ Обрабатывает последовательно цепочку
    действий от запроса пользователя до возрата итога """

    await writing_finished_data(user_id)
    mess = await returning_finished_data(user_id)

    return mess
