# main.py
"""
Main module.
"""


import ssl
import talib

from api_websocket import ws_kline
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL
from helpers import determine_trend, fetch_candles

candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100)
timestamp = candles['timestamp'].to_numpy()[-1]
rsi = talib.RSI(candles['close'].to_numpy())
sma = talib.SMA(rsi, timeperiod=14)
print(timestamp, '| RSI:', rsi[-1], '| SMA:', sma[-1])

TREND = determine_trend(candles)
print('determine_trend:', TREND.upper())

ws = ws_kline(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
