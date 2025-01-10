# helpers/determine_trend.py
"""
Determine trend module.
"""


from decouple import config
# from binance.enums import *
from binance.enums import KLINE_INTERVAL_1MINUTE, KLINE_INTERVAL_5MINUTE

API_WEBSOCKET_URL = config('API_WEBSOCKET_URL')

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

TRADE_SYMBOL = 'ETHUSDT'
TRADE_VALUE = 20
TRADE_QUANTITY = 0.05

KLINE_INTERVAL = KLINE_INTERVAL_1MINUTE
KLINE_TREND_INTERVAL = KLINE_INTERVAL_5MINUTE

# Trend
BULLISH = "bullish"
BEARISH = "bearish"
