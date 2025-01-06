import pprint

from api.binance_client import client
from constants import TRADE_SYMBOL


def get_open_orders(symbol):
    try:
        orders = client.get_open_orders(symbol=symbol)

        return orders

    except Exception as e:
        print(f"Błąd podczas pobierania otwartych zleceń: {e}")

    return None

# pprint.pprint(get_open_orders(symbol=TRADE_SYMBOL))
