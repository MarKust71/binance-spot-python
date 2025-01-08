# helpers/determine_trend.py
"""
Determine trend module.
"""


from helpers.calculate_ema import calculate_ema
from helpers.fetch_candles import fetch_candles


def determine_trend(symbol, interval) -> str:
    """
    This function does something.

    Args:
        symbol: Description of param1.
        interval: Description of param1.

    Returns:
        Trend direction
    """
    data_frame = fetch_candles(symbol, interval)

    if data_frame is not None:
        data_frame['ema_50'] = calculate_ema(data_frame['close'], 50)
        data_frame['ema_200'] = calculate_ema(data_frame['close'], 200)
        if data_frame['ema_50'].iloc[-1] > data_frame['ema_200'].iloc[-1]:
            return "bullish"  # Trend wzrostowy
        if data_frame['ema_50'].iloc[-1] < data_frame['ema_200'].iloc[-1]:
            return "bearish"  # Trend spadkowy

    return ''
