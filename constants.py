# helpers/constants.py
"""
App constants module.
"""
import enum

from binance import KLINE_INTERVAL_1MINUTE, KLINE_INTERVAL_5MINUTE
from decouple import config


API_WEBSOCKET_URL = config('API_WEBSOCKET_URL')
APPLY_TAKE_PROFIT = bool(config('APPLY_TAKE_PROFIT') == 'True')
APPLY_TAKE_PROFIT_SAFE = bool(config('APPLY_TAKE_PROFIT_SAFE') == 'True')

TP_SL_FACTOR = float(config('TP_SL_FACTOR'))
TP_SL = float(config('TP_SL'))

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

TRADE_SYMBOL = 'ETHUSDT'
TRADE_VALUE = 3 * 20
TRADE_QUANTITY = 0.05

KLINE_INTERVAL = KLINE_INTERVAL_1MINUTE
KLINE_TREND_INTERVAL = KLINE_INTERVAL_5MINUTE

# Trend
class Trend(enum.Enum):
    """
    Enum representing different market trends.
    """
    BULLISH = "bullish"
    BEARISH = "bearish"
    NONE = "none"
    BROKEN = "broken"

# Swing
SWING_HIGH = "swing_high"
SWING_LOW = "swing_low"

# Signal
SIGNAL_HIGH = "signal_high"
SIGNAL_LOW = "signal_low"

# Side
class Side(enum.Enum):
    """
    Enum representing the sides of a trade.
    """
    SELL = "sell"
    BUY = "buy"

# Trade signals
class TradeSignal(enum.Enum):
    """
    Enum representing different trade signals.
    """
    SELL = "sell"
    BUY = "buy"
    NONE = "none"

# Reason
class Reason(enum.Enum):
    """
    Enum representing the reasons of updating order.
    """
    STOP_LOSS = "STOP LOSS"
    TAKE_PROFIT = "TAKE PROFIT"
    TAKE_PROFIT_PARTIAL = "TAKE PROFIT PARTIAL"
    TAKE_PROFIT_SAFE = "TAKE PROFIT SAFE"
    UPDATE_STOP_LOSS = "UPDATE STOP LOSS"
    NONE = "NONE"

# Trade status
class TradeStatus(enum.Enum):
    """
    Enum representing the status of a trade.
    """
    OPEN = "open"
    PARTIAL = "partial"
    CLOSED = "closed"
    SAFE = "safe"
    NONE = "none"
