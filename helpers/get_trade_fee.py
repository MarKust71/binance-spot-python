import pprint

from api.binance_client import client
from constants import TRADE_SYMBOL


def get_trade_fee(symbol=None):
    try:
        fee = client.get_trade_fee(symbol=symbol)

        return fee

    except Exception as e:
        print(f"Błąd podczas pobierania opłat: {e}")

    return None


if __name__ == '__main__':
    pprint.pprint(get_trade_fee(symbol=TRADE_SYMBOL))
