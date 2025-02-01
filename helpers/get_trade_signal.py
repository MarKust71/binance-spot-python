# get_trade_signa.py
"""
Get trade signal module.
"""


from constants import SWING_HIGH, SIGNAL_HIGH, SWING_LOW, SIGNAL_LOW, TradeSignal, Trend
from helpers import get_rsi_signals


def get_trade_signal(trend, data):
    """
    Get trade signal based on RSI signal and trend.

    :param trend: str: Trend.
    :param data: pandas.DataFrame: Data.

    :return: str: Trade signal.
    """

    rsi_signals = get_rsi_signals(data['rsi'].to_numpy())

    signal_high = rsi_signals[SWING_HIGH] and rsi_signals[SIGNAL_HIGH]
    signal_low = rsi_signals[SWING_LOW] and rsi_signals[SIGNAL_LOW]

    if signal_high or signal_low:
        print('\n**')
        print('determine_trend:', trend.value.upper())

        for i in range(-3, 0):
            print(data['timestamp'].iloc[i].strftime('%Y-%m-%d %H:%M:%S'),
                  f'| price: {data['close'].to_numpy()[i]:,.2f}',
                  f'| RSI: {data['rsi'].to_numpy()[i]:,.2f}',
                  f'| SMA: {data['sma'].to_numpy()[i]:,.2f}',
                  f'| ATR: {data['atr'].to_numpy()[i]:,.2f}'
                  )

        if rsi_signals[SWING_HIGH] and rsi_signals[SIGNAL_HIGH]:
            print('   RSI swing HIGH:', rsi_signals[SWING_HIGH],
                  '| RSI signal HIGH:', rsi_signals[SIGNAL_HIGH]
                  )

        if rsi_signals[SWING_LOW] and rsi_signals[SIGNAL_LOW]:
            print('   RSI swing LOW:', rsi_signals[SWING_LOW],
                  '| RSI signal LOW:', rsi_signals[SIGNAL_LOW]
                  )

    if rsi_signals[SWING_HIGH] and rsi_signals[SIGNAL_HIGH] and trend == Trend.BEARISH:
        return TradeSignal.SELL

    if rsi_signals[SWING_LOW] and rsi_signals[SIGNAL_LOW] and trend == Trend.BULLISH:
        return TradeSignal.BUY

    return TradeSignal.NONE
