# api_websocket/handle_websocket_message.py
"""
Binance handle websocket message module.
"""
import json
import itertools
import pandas as pd

from api_websocket.log_candle_close import log_candle_close
from constants import TRADE_SYMBOL, KLINE_INTERVAL, KLINE_TREND_INTERVAL
from db.utils import db_add_trade
from helpers import fetch_candles, get_rsi_signals

LIMIT = 200
TREND_LIMIT = 200
DELAY = 0
FRACTALS_PERIODS = 8

spinner = itertools.cycle(["|", "/", "-", "\\"])


def handle_websocket_message(message) -> None:
    """
    This function handles websocket message.

    Args:
        message: Description of param1.

    Returns:
        None
    """
    print(f"\r{next(spinner)}", end="", flush=True)

    if not hasattr(handle_websocket_message, 'LAST_CLOSE'):
        handle_websocket_message.LAST_CLOSE = None

    json_message = json.loads(message)
    event_time_utc = pd.to_datetime(json_message['E'], unit='ms', utc=True)

    candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, end_time=None
    )
    trend_candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=TREND_LIMIT, end_time=None
    )

    close_time_utc = pd.to_datetime(candles['close_time'].to_numpy()[-1], unit='ms', utc=True)
    is_candle_closed = close_time_utc < event_time_utc

    if is_candle_closed and handle_websocket_message.LAST_CLOSE != close_time_utc:
        handle_websocket_message.LAST_CLOSE = close_time_utc

        candle_data = {
            "close_price": candles['close'].to_numpy()[-1],
            "open_price": candles['open'].to_numpy()[-1],
            "rsi": candles['rsi'].to_numpy()[-1],
            "atr": candles['atr'].to_numpy()[-1],
            "close_time_utc": close_time_utc,
        }

        rsi_signals = get_rsi_signals(candles['rsi'].to_numpy())

        log_candle_close(candle_data, rsi_signals)

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
