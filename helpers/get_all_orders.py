import pprint

from api import client
from constants import TRADE_SYMBOL


def get_all_orders(symbol):
    try:
        orders = client.get_all_orders(symbol=symbol)

        return orders

    except Exception as e:
        print(f"Błąd podczas pobierania zleceń: {e}")

    return None


if __name__ == '__main__':
    pprint.pprint(get_all_orders(symbol=TRADE_SYMBOL))
