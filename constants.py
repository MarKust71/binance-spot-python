# helpers/constants.py
"""
App constants module.
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
TREND_BULLISH = "bullish"
TREND_BEARISH = "bearish"
TREND_NONE = "none"

# Swing
SWING_HIGH = "swing_high"
SWING_LOW = "swing_low"

# Signal
SIGNAL_HIGH = "signal_high"
SIGNAL_LOW = "signal_low"

# Trade signals
TRADE_SIGNAL_BUY = "buy"
TRADE_SIGNAL_SELL = "sell"
TRADE_SIGNAL_NONE = "none"
