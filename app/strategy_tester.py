# strategy_tester.py
"""
Strategy tester module.
"""

import pandas as pd
import talib

from constants import TRADE_SYMBOL, KLINE_INTERVAL, \
    TRADE_SIGNAL_SELL, TRADE_SIGNAL_BUY, TRADE_SIGNAL_NONE, KLINE_TREND_INTERVAL
from helpers import (determine_trend, fetch_candles, get_trade_signal, set_fractals)

LIMIT=1000
SCOPE=2
TREND_LIMIT=1000
FRACTALS_PERIODS=20
DELAY=5

candles = fetch_candles(
    symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, endTime=None
)
trend_candles = fetch_candles(
    symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=TREND_LIMIT, endTime=None
)

# tc = set_fractals(trend_candles, periods=FRACTALS_PERIODS)
# fr = tc[tc['Fractal_Up'].notnull() | tc['Fractal_Down'].notnull()][['timestamp', 'Fractal_Down', 'Fractal_Up']]
# print(fr)
# fr.to_csv('fractals.csv')

candles.to_csv('candles.csv')
trend_candles.to_csv('trend_candles.csv')


for i in range(0, len(candles) - SCOPE + 1):

    data = candles.iloc[:SCOPE + i]
    rsi = talib.RSI(data['close'].to_numpy())
    sma = talib.SMA(rsi, timeperiod=14)

    trend_data = trend_candles[
        trend_candles['timestamp']
        <= data['timestamp'].iloc[-1] - pd.Timedelta(minutes=DELAY * FRACTALS_PERIODS)
    ]
    atr = talib.ATR(trend_data['high'].to_numpy(), trend_data['low'].to_numpy(),
                    trend_data['close'].to_numpy(), timeperiod=14)
    trend_data=set_fractals(trend_data, periods=FRACTALS_PERIODS)

    trend = determine_trend(trend_data)
    trade_signal = get_trade_signal(trend, data)

    if trade_signal != TRADE_SIGNAL_NONE:
        fractals = trend_data[
            trend_data['Fractal_Up'].notnull()
            | trend_data['Fractal_Down'].notnull()
        ][['timestamp', 'Fractal_Down', 'Fractal_Up']]
        print(fractals[
                  fractals['Fractal_Up'].notnull() | fractals['Fractal_Down'].notnull()
              ][['timestamp', 'Fractal_Down', 'Fractal_Up']].tail(5))

        print('timestamp:', data['timestamp'].iloc[-1])

        if trade_signal == TRADE_SIGNAL_SELL:
            print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')

        if trade_signal == TRADE_SIGNAL_BUY:
            print('***** BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY *****')

        print('\n')

    # else:
    #     print(data['timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S'),
    #           f'| price: {data['close'].to_numpy()[-1]:,.2f}',
    #           f'| RSI: {rsi[-1]:,.2f}',
    #           f'| SMA: {sma[-1]:,.2f}', '| RSI swing:',
    #           rsi_signals["swing"], '| RSI signal:', rsi_signals["signal"],
    #           '| Trend:', trend.upper()
    # #           f'| EMA50: {calculate_ema(trend_data['close'], 50).iloc[-1]:,.2f}',
    # #           f'| EMA200: {calculate_ema(trend_data['close'], 200).iloc[-1]:,.2f}'
    #           )


if __name__ == '__main__':
    pass
