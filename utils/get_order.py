# utils/get_order.py
"""
Get order module.
"""


import pprint
from requests.exceptions import HTTPError, ConnectionError as RequestsConnectionError, Timeout
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
    except (HTTPError, RequestsConnectionError, Timeout) as e:
        print(f"Error while fetching order: {e}")
    except (ValueError, KeyError, TypeError) as e:
        print(f"An unexpected error occurred: {e}")

    return []


if __name__ == '__main__':
    pprint.pprint(get_order(symbol=TRADE_SYMBOL, order_id=629088))
