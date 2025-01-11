# helpers/determine_trend.py
"""
Determine trend module.
"""


from constants import BULLISH, BEARISH
from helpers.calculate_ema import calculate_ema


def determine_trend(data_frame) -> str:
    """
    This function does something.

    Args:
        symbol: Description of param1.
        interval: Description of param1.

    Returns:
        Trend direction
    """


    if data_frame is not None:
        data_frame['ema_50'] = calculate_ema(data_frame['close'], 50)
        data_frame['ema_200'] = calculate_ema(data_frame['close'], 200)
        if data_frame['ema_50'].iloc[-1] > data_frame['ema_200'].iloc[-1]:
            return BULLISH  # Trend wzrostowy
        if data_frame['ema_50'].iloc[-1] < data_frame['ema_200'].iloc[-1]:
            return BEARISH  # Trend spadkowy

    return ''
