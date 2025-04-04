# api_websocket/handle_websocket_message.py
"""
Binance handle websocket message module.
"""
import itertools
import json
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

    json_message = json.loads(message)
    is_candle_closed = json_message['k']['x']

    if not is_candle_closed:
        return

    candle_close_time = json_message['k']['T']

    candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, end_time=candle_close_time
    )
    trend_candles = fetch_candles(
        symbol=TRADE_SYMBOL,
        interval=KLINE_TREND_INTERVAL,
        limit=TREND_LIMIT,
        end_time=candle_close_time
    )

    close_time_utc = pd.to_datetime(candles['close_time'].to_numpy()[-1], unit='ms', utc=True)

    candle_data = {
        "close_price": candles['close'].to_numpy()[-1],
        "open_price": candles['open'].to_numpy()[-1],
        "rsi": candles['rsi'].to_numpy()[-1],
        "atr": candles['atr'].to_numpy()[-1],
        "close_time_utc": close_time_utc.floor('min'),
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
