# strategy_tester.py
"""
Strategy tester module.
"""


import pandas as pd
import numpy as np

from constants import TRADE_SYMBOL, KLINE_INTERVAL, \
    TRADE_SIGNAL_SELL, TRADE_SIGNAL_BUY, TRADE_SIGNAL_NONE, KLINE_TREND_INTERVAL
from db import TradeRepository, Side
from helpers import (determine_trend, fetch_candles, get_trade_signal, set_fractals)

LIMIT=1000
SCOPE=2
TREND_LIMIT=1000
FRACTALS_PERIODS=20
DELAY=0

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

# candles.to_csv('candles.csv')
# trend_candles.to_csv('trend_candles.csv')

repo = TradeRepository()

for i in range(0, len(candles) - SCOPE + 1):

    data = candles.iloc[:SCOPE + i]

    trend_data = trend_candles[
        trend_candles['timestamp']
        <= data['timestamp'].iloc[-1] - pd.Timedelta(minutes=DELAY * FRACTALS_PERIODS)
    ]
    trend_data=set_fractals(trend_data, periods=FRACTALS_PERIODS)

    trend = determine_trend(trend_data.iloc[:-FRACTALS_PERIODS])
    trade_signal = get_trade_signal(trend, data)

    if trade_signal != TRADE_SIGNAL_NONE:
        fractals = trend_data[
            trend_data['Fractal_Up'].notnull()
            | trend_data['Fractal_Down'].notnull()
        ][['timestamp', 'Fractal_Down', 'Fractal_Up']]
        print('fractals:')
        print(fractals[
                  fractals['Fractal_Up'].notnull() | fractals['Fractal_Down'].notnull()
              ][['timestamp', 'Fractal_Down', 'Fractal_Up']].tail(5))

        # print('ATR:', trend_data['timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S'),
        #       f'| price: {trend_data['close'].to_numpy()[-1]:,.2f}',
        #       f'| RSI: {trend_data['rsi'].to_numpy()[-1]:,.2f}',
        #       f'| SMA: {trend_data['sma'].to_numpy()[-1]:,.2f}',
        #       f'| ATR: {trend_data['atr'].to_numpy()[-1]:,.2f}')

        # print('data:')
        # print(data[['timestamp', 'close', 'rsi', 'sma', 'atr']].tail(5))
        # print('trend_data:')
        # print(trend_data[['timestamp', 'close', 'rsi', 'sma', 'atr']].tail(5))
        print('trend_data:')
        print(trend_data[['timestamp', 'close', 'rsi', 'sma', 'atr']].tail(1))

        print('timestamp:', data['timestamp'].iloc[-1])

        if trade_signal != TRADE_SIGNAL_NONE:
            print(f'ATR: {trend_data["atr"].iloc[-1]:,.2f}')

        if trade_signal == TRADE_SIGNAL_SELL:
            repo.add_trade(
                date_time=data['timestamp'].iloc[-1],
                symbol=TRADE_SYMBOL,
                side=Side.SELL,
                price=data["close"].to_numpy()[-1],
                atr=np.round(trend_data["atr"].to_numpy()[-1], 2)
            )
            print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')

        if trade_signal == TRADE_SIGNAL_BUY:
            repo.add_trade(
                date_time=data['timestamp'].iloc[-1],
                symbol=TRADE_SYMBOL,
                side=Side.BUY,
                price=data["close"].to_numpy()[-1],
                atr=np.round(trend_data["atr"].to_numpy()[-1], 2)
            )
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

repo.close()

if __name__ == '__main__':
    pass

    # repo = TradeRepository()
    #
    # # Dodanie przykładowej transakcji
    # repo.add_trade(symbol="ETHUSDT", side=Side.BUY, price=3125.50, atr=8.8)
    #
    # # Pobranie i wyświetlenie transakcji
    # trades = repo.get_all_trades()
    # for trade in trades:
    #     print(trade)
    #
    # trade = repo.get_trade_by_id(33)
    # print(trade)
    # print(trade.stop_loss)
    #
    # repo.close()
