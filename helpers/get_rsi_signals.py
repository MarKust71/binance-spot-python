# helpers/get_rsi_signals.py
"""
Calculate RSI signals module.
"""


import talib

def get_rsi_signals(rsi: talib.RSI) -> dict:
    rsi_signals = {
        "swing_high": rsi[-2] > rsi[-1] and rsi[-2] > rsi[-3],
        "swing_low": rsi[-2] < rsi[-1] and rsi[-2] < rsi[-3],
        "signal_high": rsi[-2] > 70,
        "signal_low": rsi[-2] < 30
    }

    rsi_signals["swing"] = rsi_signals["swing_high"] or rsi_signals["swing_low"]
    rsi_signals["signal"] = rsi_signals["signal_high"] or rsi_signals["signal_low"]

    return rsi_signals
