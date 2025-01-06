import pprint, talib, json

import pandas as pd

from constants import RSI_PERIOD, RSI_OVERBOUGHT, TRADE_VALUE, TRADE_SYMBOL, RSI_OVERSOLD, KLINE_INTERVAL, \
    KLINE_TREND_INTERVAL
from helpers import create_order, fetch_candles, determine_trend

closes = []
in_position = False
last_close = None


def handle_message(message):
    global closes, in_position, last_close

    # print('received message')
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    event_time = pd.to_datetime(json_message['E'], unit='ms')

    kline = json_message['k']

    # print(event_time, kline['c'], kline['x'])
    # pprint.pprint(kline)

    candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100)
    # rsi = talib.RSI(candles['close'].to_numpy())
    # sma = talib.SMA(rsi, timeperiod=14)
    # close_time = pd.to_datetime(numpy.array(candles['close_time'])[-1], unit='ms')
    close_time = pd.to_datetime(candles['close_time'].to_numpy()[-1], unit='ms')
    # print(event_time, 'price:', candles['close'].to_numpy()[-1], '| RSI:', rsi[-1], '| SMA:', sma[-1])

    is_candle_closed = (close_time < event_time)

    if is_candle_closed and last_close != close_time:
        last_close = close_time

        # trend = determine_trend(TRADE_SYMBOL, KLINE_TREND_INTERVAL)
        # print('determine_trend:', trend.upper())

        rsi = talib.RSI(candles['close'].to_numpy())
        sma = talib.SMA(rsi, timeperiod=14)
        # print(event_time, 'price:', candles['close'].to_numpy()[-1], '| RSI:', rsi[-1], '| SMA:', sma[-1])

        candle = {
            "timestamp": candles['timestamp'].to_numpy()[-2],
            "close": candles['close'].to_numpy()[-2],
            "rsi": rsi[-2],
            "sma": sma[-2]
        }

        rsi_swing_high = (rsi[-1] < rsi[-2] and rsi[-2] > rsi[-3])
        rsi_swing_low = (rsi[-1] < rsi[-2] and rsi[-2] < rsi[-3])
        rsi_swing = rsi_swing_high or rsi_swing_low
        rsi_signal_high = rsi[-2] > 70
        rsi_signal_low = rsi[-2] < 30
        rsi_signal = rsi_signal_high or rsi_signal_low

        if rsi_swing_high and rsi_signal_high:
            print('**', close_time)
            print(candles['timestamp'].to_numpy()[-3], 'price:', candles['close'].to_numpy()[-3], '| RSI:', rsi[-3], '| SMA:', sma[-3])
            print(candles['timestamp'].to_numpy()[-2], 'price:', candles['close'].to_numpy()[-2], '| RSI:', rsi[-2], '| SMA:', sma[-2])
            print(candles['timestamp'].to_numpy()[-1], 'price:', candles['close'].to_numpy()[-1], '| RSI:', rsi[-1], '| SMA:', sma[-1])
            print('   RSI swing HIGH:', rsi_swing_high, '| RSI signal HIGH:', rsi_signal_high)
            pprint.pprint(candle)
            print('\n')

        if rsi_swing_low and rsi_signal_low:
            print('**', close_time)
            print(candles['timestamp'].to_numpy()[-3], 'price:', candles['close'].to_numpy()[-3], '| RSI:', rsi[-3], '| SMA:', sma[-3])
            print(candles['timestamp'].to_numpy()[-2], 'price:', candles['close'].to_numpy()[-2], '| RSI:', rsi[-2], '| SMA:', sma[-2])
            print(candles['timestamp'].to_numpy()[-1], 'price:', candles['close'].to_numpy()[-1], '| RSI:', rsi[-1], '| SMA:', sma[-1])
            print('   RSI swing LOW:', rsi_swing_low, '| RSI signal LOW:', rsi_signal_low)
            pprint.pprint(candle)
            print('\n')
    else:
        last_close = None


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
