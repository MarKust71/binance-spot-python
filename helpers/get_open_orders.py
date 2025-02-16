# helpers/determine_trend.py
"""
Determine trend module.
"""


import pprint

from api.binance_client import client
from constants import TRADE_SYMBOL


def get_open_orders(symbol) -> list:
    """
    This function does something.

    Args:
        symbol: Description of param1.

    Returns:
        List of open orders
    """
    try:
        orders = client.get_open_orders(symbol=symbol)

        return orders

    except (ValueError, KeyError, TypeError) as e:
        print(f"Błąd podczas pobierania otwartych zleceń: {e}")

    return []


if __name__ == '__main__':
    pprint.pprint(get_open_orders(symbol=TRADE_SYMBOL))
