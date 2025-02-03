# api/handle_websocket_message.py
"""
Binance handle websocket message module.
"""


import json
# import talib
import pandas as pd
# from binance import SIDE_SELL, SIDE_BUY
import numpy as np

from constants import TRADE_SYMBOL, KLINE_INTERVAL, TRADE_VALUE, KLINE_TREND_INTERVAL, TradeSignal, Reason, Side
from db.repositories import TradeRepository
from helpers import fetch_candles, determine_trend, get_trade_signal, set_fractals
# from helpers.create_order import create_order

# from helpers import fetch_candles, determine_trend, get_rsi_signals, get_trade_signal, set_fractals
# from helpers.calculate_ema import calculate_ema
# from helpers.create_order import create_order

# closes = []
# IN_POSITION = False

LIMIT = 200
TREND_LIMIT = 200
DELAY = 0
FRACTALS_PERIODS = 8

LAST_CLOSE = None

def handle_websocket_message(message) -> None:
    """
    This function handles websocket message.

    Args:
        message: Description of param1.

    Returns:
        None
    """


    global LAST_CLOSE

    trades_repo = TradeRepository()

    json_message = json.loads(message)
    event_time = pd.to_datetime(json_message['E'], unit='ms')
    # kline = json_message['k']

    candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, endTime=None)
    trend_candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=TREND_LIMIT, endTime=None
    )


    close_time = pd.to_datetime(candles['close_time'].to_numpy()[-1], unit='ms')
    is_candle_closed = close_time < event_time


    if not is_candle_closed or LAST_CLOSE == close_time:
        return

    LAST_CLOSE = close_time
    print(f'Candle closed: {close_time}')

    current_high = candles['high'].to_numpy()[-1]
    current_low = candles['low'].to_numpy()[-1]
    current_date = candles['timestamp'].iloc[-1]

    trend_data = trend_candles[
        trend_candles['timestamp']
        <= candles['timestamp'].iloc[-1] - pd.Timedelta(minutes=DELAY * FRACTALS_PERIODS)
        ]
    trend_data=set_fractals(trend_data, periods=FRACTALS_PERIODS)
    last_fractals = trend_data[
        trend_data['Fractal_Up'].notnull()
        | trend_data['Fractal_Down'].notnull()
        ][['timestamp', 'Fractal_Down', 'Fractal_Up']].tail(4)

    trend = determine_trend(trend_data.iloc[:-FRACTALS_PERIODS])
    trade_signal = get_trade_signal(trend, candles, fractals=last_fractals)

    new_trade_id = None

    if trade_signal != TradeSignal.NONE:
        print('trend_data:')
        print(trend_data[['timestamp', 'close', 'rsi', 'sma', 'atr']].tail(1))

        print('timestamp:', candles['timestamp'].iloc[-1])

        quantity=round(TRADE_VALUE / candles["close"].to_numpy()[-1], 4)

        if trade_signal != TradeSignal.NONE:
            print(f'ATR: {trend_data["atr"].iloc[-1]:,.2f}')
            print(f'QTY: {quantity}')

        if trade_signal == TradeSignal.SELL:
            new_trade_id = trades_repo.add_trade(
                date_time=candles['timestamp'].iloc[-1],
                symbol=TRADE_SYMBOL,
                side=Side.SELL,
                price=candles["close"].to_numpy()[-1],
                quantity=quantity,
                atr=np.round(trend_data["atr"].to_numpy()[-1], 2)
            )
            # order_succeeded = create_order(Side.SELL, quantity, TRADE_SYMBOL)
            print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')

        if trade_signal == TradeSignal.BUY:
            new_trade_id = trades_repo.add_trade(
                date_time=candles['timestamp'].iloc[-1],
                symbol=TRADE_SYMBOL,
                side=Side.BUY,
                price=candles["close"].to_numpy()[-1],
                quantity=quantity,
                atr=np.round(trend_data["atr"].to_numpy()[-1], 2)
            )
            # order_succeeded = create_order(Side.BUY, quantity, TRADE_SYMBOL)
            print('***** BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY *****')

        print('\n')

    stored_trades = [trade for trade in trades_repo.get_all_trades() if trade.id != new_trade_id and not trade.is_closed]

    for trade in stored_trades:
        trade_closed = False
        reason = Reason.NONE
        profit = 0
        current_price = 0

        if trade.date_time >= current_date:
            continue

        if trade.side == Side.BUY or trade.side == Side.SELL:
            if trade.side == Side.BUY:
                if current_low <= trade.stop_loss:
                    reason = Reason.STOP_LOSS
                    profit = round(trade.quantity * (current_low - trade.price), 2)
                    current_price = current_low
                    trade_closed = True
                elif current_high >= trade.take_profit:
                    reason = Reason.TAKE_PROFIT
                    profit = round(trade.quantity * (current_high - trade.price), 2)
                    current_price = current_high
                    trade_closed = True

            if trade.side == Side.SELL:
                if current_high >= trade.stop_loss:
                    reason = Reason.STOP_LOSS
                    profit = round(trade.quantity * (trade.price - current_high), 2)
                    current_price = current_high
                    trade_closed = True
                elif current_low <= trade.take_profit:
                    reason = Reason.TAKE_PROFIT
                    profit = round(trade.quantity * (trade.price - current_low), 2)
                    current_price = current_low
                    trade_closed = True

        if trade_closed:
            trades_repo.update_trade(
                trade.id,
                is_closed=True,
                close_price=current_price,
                close_date_time = current_date,
                quantity=0,  # Trade is fully closed
                profit=trade.profit if trade.profit is not None else 0 + profit
            )

            print(f'ID: {trade.id} price: {current_price} date: {current_date} profit: {profit} ***** {reason.value} *****')


    # if is_candle_closed and LAST_CLOSE != close_time:
    #     LAST_CLOSE = close_time
    #
    #     rsi = talib.RSI(candles['close'].to_numpy())
    #     sma = talib.SMA(rsi, timeperiod=14)
    #
    #     candle = {
    #         "timestamp": candles['timestamp'].to_numpy()[-1],
    #         "close": candles['close'].to_numpy()[-1],
    #         "rsi": rsi[-1],
    #         "sma": sma[-1]
    #     }
    #
    #     rsi_signals = get_rsi_signals(rsi)
    #
    #     trade_signal = get_trade_signal(trend, candles)
    #
    #     if trade_signal != TradeSignal.NONE:
    #         quantity = round(TRADE_VALUE / float(candle['close']), 4)
    #         order_succeeded = None
    #
    #         if trade_signal == TradeSignal.SELL:
    #             print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')
    #             order_succeeded = create_order(SIDE_SELL, quantity, TRADE_SYMBOL)
    #
    #         if trade_signal == TradeSignal.BUY:
    #             print('***** BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY *****')
    #             order_succeeded = create_order(SIDE_BUY, quantity, TRADE_SYMBOL)
    #
    #         print(f'Order succeeded: {order_succeeded}\n')
    #
    #     else:
    #         print(candles['timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S'), f'| price: {candles['close'].to_numpy()[-1]:,.2f}',
    #         # print(candles['timestamp'].to_numpy()[-1], f'price: {candles['close'].to_numpy()[-1]:,.2f}',
    #         # print(candles['timestamp'].to_numpy()[-1], f'price: {candles['close'].to_numpy()[-1]:,.2f}',
    #             f'| RSI: {rsi[-1]:,.2f}',
    #             f'| SMA: {sma[-1]:,.2f}', '| RSI swing:',
    #             rsi_signals["swing"], '| RSI signal:', rsi_signals["signal"],
    #             '| Trend:', trend.value.upper(),
    #             f'| EMA50: {calculate_ema(trend_candles['close'], 50).iloc[-1]:,.2f}',
    #             f'| EMA200: {calculate_ema(trend_candles['close'], 200).iloc[-1]:,.2f}')


    trades_repo.close()





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
#     candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100, endTime=None)
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
