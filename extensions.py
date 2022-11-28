import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(what: str, into: str, amount: str):

        if what == into:
            raise ConvertionException(f"Невозможно перевести одинаковые валюты {into}.")

        try:
            what_ticker = keys[what]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {what}")

        try:
            into_ticker = keys[into]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {into}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={what_ticker}&tsyms={into_ticker}")
        total_amount = json.loads(r.content)[keys[into]]

        return total_amount