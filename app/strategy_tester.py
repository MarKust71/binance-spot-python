# strategy_tester.py
"""
Strategy tester module.
"""


import pandas as pd
import numpy as np

from constants import TRADE_SYMBOL, KLINE_INTERVAL, KLINE_TREND_INTERVAL, TradeSignal, TRADE_VALUE, Side
from db.repositories import TradeRepository
from db.utils import db_update_trades
from helpers import (determine_trend, fetch_candles, get_trade_signal, set_fractals)

LIMIT = 1000
SCOPE = 2
TREND_LIMIT = 1000
FRACTALS_PERIODS = 8
DELAY = 0

def strategy_tester():
    """
    Strategy tester function.
    """
    pass


    candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, end_time=None
    )
    trend_candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=TREND_LIMIT, end_time=None
    )

    # tc = set_fractals(trend_candles, periods=FRACTALS_PERIODS)
    # fr = tc[tc['Fractal_Up'].notnull() | tc['Fractal_Down'].notnull()][['timestamp', 'Fractal_Down', 'Fractal_Up']]
    # print(fr)
    # fr.to_csv('fractals.csv')

    # candles.to_csv('candles.csv')
    # trend_candles.to_csv('trend_candles.csv')



    for i in range(0, len(candles) - SCOPE + 1):

        data = candles.iloc[:SCOPE + i]

        current_high = data['high'].to_numpy()[-1]
        current_low = data['low'].to_numpy()[-1]
        current_date = data['timestamp'].iloc[-1]

        trend_data = trend_candles[
            trend_candles['timestamp']
            <= data['timestamp'].iloc[-1] - pd.Timedelta(minutes=DELAY * FRACTALS_PERIODS)
        ]
        trend_data=set_fractals(trend_data, periods=FRACTALS_PERIODS)
        last_fractals = trend_data[
            trend_data['Fractal_Up'].notnull()
            | trend_data['Fractal_Down'].notnull()
            ][['timestamp', 'Fractal_Down', 'Fractal_Up']].tail(4)

        trend = determine_trend(trend_data.iloc[:-FRACTALS_PERIODS])
        trade_signal = get_trade_signal(trend, data, fractals=last_fractals)

        if trade_signal != TradeSignal.NONE:
            print('trend_data:')
            print(trend_data[['timestamp', 'close', 'rsi', 'sma', 'atr']].tail(1))

            print('timestamp:', data['timestamp'].iloc[-1])

            if trade_signal != TradeSignal.NONE:
                print(f'ATR: {trend_data["atr"].iloc[-1]:,.2f}')
                print(f'QTY: {round(TRADE_VALUE / data["close"].to_numpy()[-1], 4)}')

                trades_repo = TradeRepository()
                trades_repo.add_trade(
                    date_time=data['timestamp'].iloc[-1],
                    symbol=TRADE_SYMBOL,
                    side=Side.SELL if trade_signal == TradeSignal.SELL else Side.BUY,
                    price=data["close"].to_numpy()[-1],
                    quantity=round(TRADE_VALUE / data["close"].to_numpy()[-1], 4),
                    atr=np.round(trend_data["atr"].to_numpy()[-1], 2)
                )
                trades_repo.close()

            if trade_signal == TradeSignal.SELL:
                print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')

            if trade_signal == TradeSignal.BUY:
                print('***** BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY *****')

            print('\n')


        db_update_trades(
            symbol=TRADE_SYMBOL,
            price=data["close"].to_numpy()[-1],
            timestamp=data['timestamp'].iloc[-1],
        )



if __name__ == '__main__':
    strategy_tester()

    # trades_repo = TradeRepository()
    #
    # # Dodanie przykładowej transakcji
    # trades_repo.add_trade(symbol="ETHUSDT", side=Side.BUY, price=3125.50, atr=8.8)
    #
    # # Pobranie i wyświetlenie transakcji
    # trades = trades_repo.get_all_trades()
    # for trade in trades:
    #     print(trade)
    #
    # trade = trades_repo.get_trade_by_id(33)
    # print(trade)
    # print(trade.stop_loss)
    #
    # trades_repo.close()
