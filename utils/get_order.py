# utils/get_order.py
"""
Get order module.
"""


import pprint

from api import client
from constants import TRADE_SYMBOL


def get_order(symbol, order_id) -> list:
    """
    This function does something.

    Args:
        symbol: Description of param1.
        order_id: Description of param

    Returns:
        List of orders
    """
    try:
        order = client.get_order(symbol=symbol, orderId=order_id)

        return order

    except Exception as e:
        print(f"Błąd podczas pobierania zlecenia: {e}")

    return []


if __name__ == '__main__':
    pprint.pprint(get_order(symbol=TRADE_SYMBOL, order_id=629088))
