# get_trade_signa.py
"""
Get trade signal module.
"""


import pprint

from constants import TRADE_SIGNAL_BUY, SWING_HIGH, SIGNAL_HIGH, BEARISH, \
    TRADE_SIGNAL_SELL, SWING_LOW, SIGNAL_LOW, \
    BULLISH, TRADE_SIGNAL_NONE


def get_trade_signal(rsi_signals, trend, data, rsi, sma, candle):
    """
    Get trade signal based on RSI signal and trend.

    :param rsi_signal: dict: RSI signal.
    :param trend: str: Trend.
    :param data: pandas.DataFrame: Data.
    :param rsi: numpy.ndarray: RSI.
    :param sma: numpy.ndarray: SMA.
    :param candle: dict: Candle.

    :return: str: Trade signal.
    """

    signal_high = rsi_signals[SWING_HIGH] and rsi_signals[SIGNAL_HIGH]
    signal_low = rsi_signals[SWING_LOW] and rsi_signals[SIGNAL_LOW]

    if signal_high or signal_low:
        print('\n**')
        print('determine_trend:', trend.upper())
        for i in range(-3, 0):
            print(data['timestamp'].to_numpy()[i], 'price:',
                  data['close'].to_numpy()[i], '| RSI:', rsi[i], '| SMA:', sma[i])

        if rsi_signals[SWING_HIGH] and rsi_signals[SIGNAL_HIGH]:
            print('   RSI swing HIGH:', rsi_signals[SWING_HIGH], '| RSI signal HIGH:',
                  rsi_signals[SIGNAL_HIGH])

        if rsi_signals[SWING_LOW] and rsi_signals[SIGNAL_LOW]:
            print('   RSI swing LOW:', rsi_signals[SWING_LOW], '| RSI signal LOW:',
                  rsi_signals[SIGNAL_LOW])

        pprint.pprint('candle:')
        pprint.pprint(candle)
        pprint.pprint('rsi_signals:')
        pprint.pprint(rsi_signals)

    if rsi_signals[SWING_HIGH] and rsi_signals[SIGNAL_HIGH] and trend == BEARISH:
        return TRADE_SIGNAL_SELL

    if rsi_signals[SWING_LOW] and rsi_signals[SIGNAL_LOW] and trend == BULLISH:
        return TRADE_SIGNAL_BUY

    return TRADE_SIGNAL_NONE
