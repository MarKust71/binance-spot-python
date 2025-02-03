# api/handle_websocket_message.py
"""
Binance handle websocket message module.
"""


import json
import pandas as pd
import numpy as np

from constants import TRADE_SYMBOL, KLINE_INTERVAL, TRADE_VALUE, KLINE_TREND_INTERVAL, TradeSignal
from db.repositories import TradeRepository
from helpers import fetch_candles, determine_trend, get_trade_signal, set_fractals

LIMIT = 200
TREND_LIMIT = 200
DELAY = 0
FRACTALS_PERIODS = 8

LAST_CLOSE = current_date = current_low = current_high = None

def handle_websocket_message(message) -> None:
    """
    This function handles websocket message.

    Args:
        message: Description of param1.

    Returns:
        None
    """


    global LAST_CLOSE, current_date, current_low, current_high

    trades_repo = TradeRepository()

    json_message = json.loads(message)
    event_time = pd.to_datetime(json_message['E'], unit='ms')
    # kline = json_message['k']

    candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, endTime=None)
    trend_candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=TREND_LIMIT, endTime=None
    )

    # print(f'candles: {candles["close"].iloc[-1]}')

    close_time = pd.to_datetime(candles['close_time'].to_numpy()[-1], unit='ms')
    close_price = candles['close'].to_numpy()[-1]
    is_candle_closed = close_time < event_time

    if is_candle_closed and LAST_CLOSE != close_time:

        LAST_CLOSE = close_time
        print(f'Candle closed: {close_time} | price: {close_price:,.2f}')

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

        if trade_signal != TradeSignal.NONE:
            print('trend_data:')
            print(trend_data[['timestamp', 'close', 'rsi', 'sma', 'atr']].tail(1))

            print('timestamp:', candles['timestamp'].iloc[-1])

            quantity=round(TRADE_VALUE / candles["close"].to_numpy()[-1], 4)

            if trade_signal != TradeSignal.NONE:
                print(f'ATR: {trend_data["atr"].iloc[-1]:,.2f}')
                print(f'QTY: {quantity}')

                new_trade_id = trades_repo.add_trade(
                    date_time=candles['timestamp'].iloc[-1],
                    symbol=TRADE_SYMBOL,
                    side=trade_signal,
                    price=candles["close"].to_numpy()[-1],
                    quantity=quantity,
                    atr=np.round(trend_data["atr"].to_numpy()[-1], 2)
                )

                # order_succeeded = create_order(
                #     side=trade_signal,
                #     quantity=quantity,
                #     symbol=TRADE_SYMBOL
                # )

            if trade_signal == TradeSignal.SELL:
                print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')

            if trade_signal == TradeSignal.BUY:
                print('***** BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY *****')

            print('\n')


    trades_repo.close()


if __name__ == '__main__':
    pass
