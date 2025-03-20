"""
This module contains a function that logs candle close data.
"""
import pytz

from constants import RSI_OVERBOUGHT, RSI_OVERSOLD


def log_candle_close(candle_data, rsi_signals):
    """
    This function logs candle close data.

    Args:
        candle_data: Description of param1.
        rsi_signals: Description of param2.

    Returns:
        None
    """
    price_color = "\033[92m" if candle_data["close_price"] > candle_data["open_price"] \
        else "\033[91m" if candle_data["close_price"] < candle_data["open_price"] \
        else ""
    reset_price_color = "\033[0m" if price_color else ""
    rsi_color = "\033[94m" if (candle_data["rsi"] > RSI_OVERBOUGHT
                               or candle_data["rsi"] < RSI_OVERSOLD) else ""
    reset_rsi_color = "\033[0m" if rsi_color else ""
    print(
        f'\rCandle closed: {candle_data["close_time_utc"]
            .tz_convert(pytz.timezone('Europe/Warsaw'))
            .round("min")
            .strftime('%Y-%m-%d %H:%M')} '
        f'| price: {price_color}{candle_data["close_price"]:,.2f}{reset_price_color} '
        f'| RSI: {rsi_color}{candle_data["rsi"]:.2f}{reset_rsi_color} '
        f'| ATR: {candle_data["atr"]:.2f} '
        f'{">>>" if rsi_signals["swing_high"] and rsi_signals["signal"] else ""}'
        f'{"<<<" if rsi_signals["swing_low"] and rsi_signals["signal"] else ""}'
    )
