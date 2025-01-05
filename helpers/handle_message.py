import talib, numpy, json

from binance.enums import *

from constants import RSI_PERIOD, RSI_OVERBOUGHT, TRADE_VALUE, TRADE_SYMBOL, RSI_OVERSOLD
from helpers import create_order

closes = []
in_position = False


def handle_message(message):
    global closes, in_position

    # print('received message')
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message['k']
    # pprint.pprint(candle)

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all RSIs calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    # quantity = TRADE_QUANTITY
                    quantity = round(TRADE_VALUE / float(close), 6)
                    order_succeeded = create_order(SIDE_SELL, quantity, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    # quantity = TRADE_QUANTITY
                    quantity = round(TRADE_VALUE / float(close), 6)
                    order_succeeded = create_order(SIDE_BUY, quantity, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True
