from api import client
from binance.enums import *


def create_order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occurred - {}".format(e))
        return False

    return True


if __name__ == '__main__':
    print(create_order(side=SIDE_BUY, quantity=0.00055, symbol="BTCUSDT"))
