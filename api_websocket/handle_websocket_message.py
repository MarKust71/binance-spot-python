# api_websocket/handle_websocket_message.py
"""
Binance handle websocket message module.
"""


import json
import pandas as pd

from constants import TRADE_SYMBOL, KLINE_INTERVAL, KLINE_TREND_INTERVAL
from db.utils import db_add_trade
from helpers import fetch_candles, get_rsi_signals

LIMIT = 200
TREND_LIMIT = 200
DELAY = 0
FRACTALS_PERIODS = 8


def handle_websocket_message(message) -> None:
    """
    This function handles websocket message.

    Args:
        message: Description of param1.

    Returns:
        None
    """
    if not hasattr(handle_websocket_message, 'LAST_CLOSE'):
        handle_websocket_message.LAST_CLOSE = None

    json_message = json.loads(message)
    event_time = pd.to_datetime(json_message['E'], unit='ms')
    # kline = json_message['k']

    candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, end_time=None
    )
    trend_candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=TREND_LIMIT, end_time=None
    )

    close_time = pd.to_datetime(candles['close_time'].to_numpy()[-1], unit='ms')
    is_candle_closed = close_time < event_time

    if is_candle_closed and handle_websocket_message.LAST_CLOSE != close_time:
        handle_websocket_message.LAST_CLOSE = close_time
        close_price = candles['close'].to_numpy()[-1]
        rsi = candles['rsi'].to_numpy()[-1]
        rsi_signals = get_rsi_signals(candles['rsi'].to_numpy())
        print(
            f'Candle closed: {close_time} '
            f'| price: {close_price:,.2f} '
            f'| RSI: {rsi:.2f} '
            f'{">>>" if rsi_signals["swing_high"] and rsi_signals["signal"] else ""}'
            f'{"<<<" if rsi_signals["swing_low"] and rsi_signals["signal"] else ""}'
        )

        new_trade_id = db_add_trade(
            candles=candles,
            trend_candles=trend_candles,
            delay=DELAY,
            fractals_periods=FRACTALS_PERIODS,
        )

        if new_trade_id != -1 and new_trade_id is not None:
            print(f'New trade created, ID: {new_trade_id}')


if __name__ == '__main__':
    pass
