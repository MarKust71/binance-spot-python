import pprint

from api.binance_client import client
from constants import TRADE_SYMBOL


def get_my_trades(symbol):
    try:
        trades = client.get_my_trades(symbol=symbol)

        return trades

    except Exception as e:
        print(f"Błąd podczas pobierania zleceń: {e}")

    return None


if __name__ == '__main__':
    pprint.pprint(get_my_trades(symbol=TRADE_SYMBOL))
