# helpers/determine_trend.py
"""
Determine trend module.
"""


import pprint

from api.binance_client import client
from constants import TRADE_SYMBOL


def get_trade_fee(symbol=None) -> list:
    """
    This function does something.

    Args:
        symbol: Description of param1.

    Returns:
        Fees' definitions
    """
    try:
        fee = client.get_trade_fee(symbol=symbol)

        return fee

    except (ValueError, KeyError, TypeError) as e:
        print(f"Błąd podczas pobierania opłat: {e}")

    return []


if __name__ == '__main__':
    pprint.pprint(get_trade_fee(symbol=TRADE_SYMBOL))
