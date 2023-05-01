import json
import requests
from config import cur, headers


class UserException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = cur[base]
        except KeyError:
            raise UserException(f"Валюта {base} не найдена! Список доступных валют /values")

        try:
            quote_key = cur[quote]
        except KeyError:
            raise UserException(f"Валюта {quote} не найдена! Список доступных валют /values")

        if base_key == quote_key:
            raise UserException(f'Вы выбрали одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise UserException(f'Нет возможности обработать количество {amount}!')

        url = f"https://api.apilayer.com/currency_data/convert?to={quote_key}&from={base_key}&amount={amount}"
        response = requests.request("GET", url, headers=headers)
        res_raw = json.loads(response.content)
        result = round(res_raw['result'], 2)

        message = f'Цена за {amount} {base} будет {result} {quote}'

        return message
