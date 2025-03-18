# helpers/get_rsi_signals.py
"""
Calculate RSI signals module.
"""
from constants import RSI_OVERBOUGHT, RSI_OVERSOLD


def get_rsi_signals(rsi: list) -> dict:
    """
    Calculates RSI signals based on the given RSI values.

    Args:
        rsi (list): A list of RSI values.

    Returns:
        dict: A dictionary containing RSI signals.
    """
    rsi_signals = {
        "swing_high": rsi[-2] > rsi[-1] and rsi[-2] > rsi[-3],
        "swing_low": rsi[-2] < rsi[-1] and rsi[-2] < rsi[-3],
        "signal_high": rsi[-2] > RSI_OVERBOUGHT,
        "signal_low": rsi[-2] < RSI_OVERSOLD
    }

    rsi_signals["swing"] = rsi_signals["swing_high"] or rsi_signals["swing_low"]
    rsi_signals["signal"] = rsi_signals["signal_high"] or rsi_signals["signal_low"]

    return rsi_signals
