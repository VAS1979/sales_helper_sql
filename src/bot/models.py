""" Модели для работы с базой данных """
import sqlite3

from bot.processing_requests import (input_validation, processing_sql_data,
                                     convert_tuple_to_string, create_finish_string)


async def create_db_tables():
    """ Создание таблиц """
    try:
        db_connection = sqlite3.connect('db/sales_helper.db')
        create_table_query = """CREATE TABLE IF NOT EXISTS user_data (
                                user_id INTEGER PRIMARY KEY,
                                tickers TEXT)"""
        create_summary_table = """CREATE TABLE IF NOT EXISTS finish_data (
                                user_id INTEGER PRIMARY KEY,
                                datetime TEXT,
                                quotes TEXT)"""
        cursor = db_connection.cursor()
        print("Database connected")
        cursor.execute(create_table_query)
        cursor.execute(create_summary_table)
        db_connection.commit()

        db_connection.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (db_connection):
            db_connection.close()
            print("Соединение с SQLite закрыто")


async def insert_userdata(tg_id, tickers):
    """ Запись списка тикеров,
     полученных от пользователя """

    tickers = await input_validation(tickers)

    try:
        db_connection = sqlite3.connect('db/sales_helper.db')
        cursor = db_connection.cursor()

        insert_query = "INSERT INTO user_data (user_id, tickers) VALUES (?, ?)"
        update_query = "UPDATE user_data SET tickers = ? WHERE user_id = ?"
        select_query = cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (tg_id, )).fetchone()

        if select_query:
            cursor.execute(update_query, (tickers, tg_id))
            db_connection.commit()
            print("Запись успешно обновлена ", cursor.rowcount)
        else:
            cursor.execute(insert_query, (tg_id, tickers))
            db_connection.commit()
            print("Новая запись успешно вставлена в таблицу ", cursor.rowcount)

    except sqlite3.Error as error:
        print("Ошибка при работе sqlite", error)
    finally:
        if (db_connection):
            db_connection.close()
            print("Соединение с SQLite закрыто")


async def writing_finished_data(tg_id):
    """ Считывает строку пользовательского запроса
     из базы данных, записывает в бд готовый результат """

    try:
        db_connection = sqlite3.connect('db/sales_helper.db')
        cursor = db_connection.cursor()

        insert_query = "INSERT INTO finish_data (user_id, datetime, quotes) VALUES (?, ?, ?)"
        update_query = "UPDATE finish_data SET datetime = ?, quotes = ? WHERE user_id = ?"
        select_query = cursor.execute("SELECT quotes FROM finish_data WHERE user_id = ?", (tg_id, )).fetchone()
        data_query = cursor.execute("SELECT tickers FROM user_data WHERE user_id = ?", (tg_id, )).fetchone()

        final_string = await convert_tuple_to_string(data_query)

        request = await processing_sql_data(final_string)
        quotes = request['stock_quotes']
        datetime = request['datetime']

        if select_query:
            cursor.execute(update_query, (datetime, quotes, tg_id))
            db_connection.commit()
            print("Запись успешно обновлена ", cursor.rowcount)
        else:
            cursor.execute(insert_query, (tg_id, datetime, quotes))
            db_connection.commit()
            print("Новая запись успешно вставлена в таблицу ", cursor.rowcount)

    except sqlite3.Error as error:
        print("Ошибка при работе sqlite", error)
    finally:
        if (db_connection):
            db_connection.close()
            print("Соединение с SQLite закрыто")


async def returning_finished_data(tg_id):
    """ Считывает обработанные данные из базы данных,
    формирует строку и возвращает боту """

    try:
        db_connection = sqlite3.connect('db/sales_helper.db')
        cursor = db_connection.cursor()

        select_query = cursor.execute("SELECT datetime, quotes FROM finish_data WHERE user_id = ?", (tg_id, )).fetchone()
        finish_string = await create_finish_string(select_query)

        return finish_string

    except sqlite3.Error as error:
        print("Ошибка при работе sqlite", error)
    finally:
        if (db_connection):
            db_connection.close()
            print("Соединение с SQLite закрыто")
