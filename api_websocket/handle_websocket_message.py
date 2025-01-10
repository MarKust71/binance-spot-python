# api/handle_websocket_message.py
"""
Binance handle websocket message module.
"""


import pprint
import json
import talib
import pandas as pd

from constants import TRADE_SYMBOL, KLINE_INTERVAL
from helpers import fetch_candles

# closes = []
# IN_POSITION = False
# LAST_CLOSE = None

LAST_CLOSE = None

def handle_websocket_message(message) -> None:
    """
    This function does something.

    Args:
        message: Description of param1.

    Returns:
        None
    """
    # global closes, IN_POSITION, LAST_CLOSE
    global LAST_CLOSE

    json_message = json.loads(message)
    event_time = pd.to_datetime(json_message['E'], unit='ms')
    # kline = json_message['k']

    candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100)
    close_time = pd.to_datetime(candles['close_time'].to_numpy()[-1], unit='ms')
    is_candle_closed = close_time < event_time

    if is_candle_closed and LAST_CLOSE != close_time:
        LAST_CLOSE = close_time

        rsi = talib.RSI(candles['close'].to_numpy())
        sma = talib.SMA(rsi, timeperiod=14)

        candle = {
            "timestamp": candles['timestamp'].to_numpy()[-2],
            "close": candles['close'].to_numpy()[-2],
            "rsi": rsi[-2],
            "sma": sma[-2]
        }

        rsi_signals = {
            "swing_high": rsi[-2] > rsi[-1] and rsi[-2] > rsi[-3],
            "swing_low": rsi[-2] < rsi[-1] and rsi[-2] < rsi[-3],
            "signal_high": rsi[-2] > 70,
            "signal_low": rsi[-2] < 30
        }
        rsi_signals["swing"] = rsi_signals["swing_high"] or rsi_signals["swing_low"]
        rsi_signals["signal"] = rsi_signals["signal_high"] or rsi_signals["signal_low"]

        if ((rsi_signals["swing_high"] and rsi_signals["signal_high"])
                or (rsi_signals["swing_low"] and rsi_signals["signal_low"])):
            print('**', close_time)
            for i in range(-3, 0):
                print(candles['timestamp'].to_numpy()[i], 'price:',
                      candles['close'].to_numpy()[i], '| RSI:', rsi[i], '| SMA:', sma[i])

            if rsi_signals["swing_high"] and rsi_signals["signal_high"]:
                print('   RSI swing HIGH:', rsi_signals["swing_high"], '| RSI signal HIGH:',
                      rsi_signals["signal_high"])

            if rsi_signals["swing_low"] and rsi_signals["signal_low"]:
                print('   RSI swing LOW:', rsi_signals["swing_low"], '| RSI signal LOW:',
                      rsi_signals["signal_low"])

            pprint.pprint(candle)
            print('\n')
        else:
            print(candles['timestamp'].to_numpy()[-1], 'price:',
                  candles['close'].to_numpy()[-1], '| RSI:',
                  rsi[-1], '| SMA:', sma[-1], '| RSI swing:', rsi_signals["swing"])

    else:
        LAST_CLOSE = None


# def handle_websocket_message(message):
#     global closes, in_position, last_close
#
#     json_message = json.loads(message)
#
#     event_time = pd.to_datetime(json_message['E'], unit='ms')
#
#     kline = json_message['k']
#     # pprint.pprint(kline)
#
#     candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100)
#     close_time = pd.to_datetime(candles['close_time'].to_numpy()[-1], unit='ms')
#     # pprint.pprint(candles.to_numpy()[-1])
#
#     is_candle_closed = (close_time < event_time)
#
#     if is_candle_closed and last_close != close_time:
#         last_close = close_time
#
#         rsi = talib.RSI(candles['close'].to_numpy())
#         sma = talib.SMA(rsi, timeperiod=14)
#
#         candle = {
#             "timestamp": candles['timestamp'].to_numpy()[-2],
#             "close": candles['close'].to_numpy()[-2],
#             "rsi": rsi[-2],
#             "sma": sma[-2]
#         }
#
#         rsi_swing_high = rsi[-2] > rsi[-1] and rsi[-2] > rsi[-3]
#         rsi_swing_low = rsi[-2] < rsi[-1] and rsi[-2] < rsi[-3]
#         rsi_swing = rsi_swing_high or rsi_swing_low
#         rsi_signal_high = rsi[-2] > 70
#         rsi_signal_low = rsi[-2] < 30
#         rsi_signal = rsi_signal_high or rsi_signal_low
#
#         if (rsi_swing_high and rsi_signal_high) or (rsi_swing_low and rsi_signal_low):
#             print('**', close_time)
#             for i in range(-3, 0):
#                 print(candles['timestamp'].to_numpy()[i], 'price:',
#                       candles['close'].to_numpy()[i], '| RSI:', rsi[i], '| SMA:', sma[i])
#
#             if rsi_swing_high and rsi_signal_high:
#                 print('   RSI swing HIGH:', rsi_swing_high, '| RSI signal HIGH:', rsi_signal_high)
#
#             if rsi_swing_low and rsi_signal_low:
#                 print('   RSI swing LOW:', rsi_swing_low, '| RSI signal LOW:', rsi_signal_low)
#
#             pprint.pprint(candle)
#             print('\n')
#         else:
#             print(candles['timestamp'].to_numpy()[-1], 'price:',
#                   candles['close'].to_numpy()[-1], '| RSI:',
#                   rsi[-1], '| SMA:', sma[-1], '| RSI swing:', rsi_swing)
#
#
#     else:
#         last_close = None


    # is_candle_closed = candle['x']
    # close = candle['c']
    #
    # if False and is_candle_closed:
    #     print("candle closed at {}".format(close))
    #     closes.append(float(close))
    #     print("closes")
    #     print(closes)
    #
    #     if len(closes) > RSI_PERIOD:
    #         np_closes = numpy.array(closes)
    #         rsi = talib.RSI(np_closes, RSI_PERIOD)
    #         print("all RSIs calculated so far")
    #         print(rsi)
    #         last_rsi = rsi[-1]
    #         print("the current rsi is {}".format(last_rsi))
    #
    #         if last_rsi > RSI_OVERBOUGHT:
    #             if in_position:
    #                 print("Overbought! Sell! Sell! Sell!")
    #                 # quantity = TRADE_QUANTITY
    #                 quantity = round(TRADE_VALUE / float(close), 6)
    #                 order_succeeded = create_order(SIDE_SELL, quantity, TRADE_SYMBOL)
    #                 if order_succeeded:
    #                     in_position = False
    #             else:
    #                 print("It is overbought, but we don't own any. Nothing to do.")
    #
    #         if last_rsi < RSI_OVERSOLD:
    #             if in_position:
    #                 print("It is oversold, but you already own it, nothing to do.")
    #             else:
    #                 print("Oversold! Buy! Buy! Buy!")
    #                 # quantity = TRADE_QUANTITY
    #                 quantity = round(TRADE_VALUE / float(close), 6)
    #                 order_succeeded = create_order(SIDE_BUY, quantity, TRADE_SYMBOL)
    #                 if order_succeeded:
    #                     in_position = True