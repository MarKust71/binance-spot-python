# helpers/create_order.py
"""
Create order module.
"""


# from binance.enums import *
from binance.enums import ORDER_TYPE_MARKET, SIDE_SELL, SIDE_BUY
from api import client
from constants import TRADE_SYMBOL


def create_order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET) -> bool:
    """
    This function does something.

    Args:
        side: Description of param1.
        quantity: Description of param1.
        symbol: Description of param1.
        order_type: Description of param1.

    Returns:
        None
    """
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print(f"an exception occurred - {format(e)}")
        return False

    return True


if __name__ == '__main__':
    print(create_order(side=SIDE_BUY, quantity=0.0059, symbol=TRADE_SYMBOL))
