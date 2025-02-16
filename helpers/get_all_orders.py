# helpers/determine_trend.py
"""
Determine trend module.
"""


import pprint

from api import client
from constants import TRADE_SYMBOL


def get_all_orders(symbol) -> list:
    """
    This function does something.

    Args:
        symbol: Description of param1.

    Returns:
        List of orders
    """
    try:
        orders = client.get_all_orders(symbol=symbol)

        return orders

    except (ValueError, KeyError, TypeError) as e:
        print(f"Błąd podczas pobierania zleceń: {e}")

    return []


if __name__ == '__main__':
    pprint.pprint(get_all_orders(symbol=TRADE_SYMBOL))
