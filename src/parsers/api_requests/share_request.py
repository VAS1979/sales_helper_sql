"""Содержит класс для парсинга котировок акций с API MOEX"""
import requests


class ShareInfo():
    ''''
    Запрос списка котировок акций с API MOEX
    '''
    def tickers_request(self):
        '''
        Запрос к API MOEX котировального списка,
        возвращает список из пар(тикер:цена)
        '''
        response = requests.get("http://iss.moex.com/iss/engines/"
                                "stock/markets/shares/boards/TQBR/"
                                "securities.json?iss.meta=off&iss."
                                "only=marketdata&marketdata."
                                "columns=SECID,LAST", timeout=5).json()
        data = response['marketdata']['data']
        return data


request = ShareInfo()
response_data = request.tickers_request()


class SelectiveRequest():
    ''''
    Выборочный запрос котировки по акции с API MOEX
    '''
    def ticker_request(self):
        '''
        Запрос к API MOEX котировального списка,
        возвращает список из пары(тикер:цена)
        '''
        response = requests.get("http://iss.moex.com/iss/engines/"
                                "stock/markets/shares/boards/TQBR/"
                                "securities/SBER.json?iss.meta=off&iss."
                                "only=marketdata&marketdata."
                                "columns=SECID,LAST", timeout=5).json()
        data = response['marketdata']['data']
        return data


selective_request = SelectiveRequest()
selective_response_data = selective_request.ticker_request()
