# utils/get_symbol_info.py
"""
Determine trend module.
"""


import pprint

from api import client
from constants import TRADE_SYMBOL


def get_symbol_info(symbol) -> list:
    """
    This function does something.

    Args:
        symbol: Description of param1.

    Returns:
        List of orders
    """
    try:
        symbol_info = client.get_symbol_info(symbol=symbol)

        return symbol_info

    except (ValueError, KeyError, TypeError) as e:
        print(f"Błąd podczas pobierania informacji: {e}")

    return []


if __name__ == '__main__':
    pprint.pprint(get_symbol_info(symbol=TRADE_SYMBOL))
