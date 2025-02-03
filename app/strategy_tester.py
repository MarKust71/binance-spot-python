# strategy_tester.py
"""
Strategy tester module.
"""


import pandas as pd
import numpy as np

from constants import TRADE_SYMBOL, KLINE_INTERVAL, KLINE_TREND_INTERVAL, TradeSignal, Side, Reason, TRADE_VALUE
from db.repositories import TradeRepository
from helpers import (determine_trend, fetch_candles, get_trade_signal, set_fractals)

LIMIT = 1000
SCOPE = 2
TREND_LIMIT = 1000
FRACTALS_PERIODS = 8
DELAY = 0

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

trades_repo = TradeRepository()


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
    # trend = Trend.BEARISH
    trade_signal = get_trade_signal(trend, data, fractals=last_fractals)

    new_trade_id = None

    if trade_signal != TradeSignal.NONE:
        print('trend_data:')
        print(trend_data[['timestamp', 'close', 'rsi', 'sma', 'atr']].tail(1))

        print('timestamp:', data['timestamp'].iloc[-1])

        if trade_signal != TradeSignal.NONE:
            print(f'ATR: {trend_data["atr"].iloc[-1]:,.2f}')
            print(f'QTY: {round(TRADE_VALUE / data["close"].to_numpy()[-1], 4)}')

        if trade_signal == TradeSignal.SELL:
            new_trade_id = trades_repo.add_trade(
                date_time=data['timestamp'].iloc[-1],
                symbol=TRADE_SYMBOL,
                side=Side.SELL,
                price=data["close"].to_numpy()[-1],
                quantity=round(TRADE_VALUE / data["close"].to_numpy()[-1], 4),
                atr=np.round(trend_data["atr"].to_numpy()[-1], 2)
            )
            print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')

        if trade_signal == TradeSignal.BUY:
            new_trade_id = trades_repo.add_trade(
                date_time=data['timestamp'].iloc[-1],
                symbol=TRADE_SYMBOL,
                side=Side.BUY,
                price=data["close"].to_numpy()[-1],
                quantity=round(TRADE_VALUE / data["close"].to_numpy()[-1], 4),
                atr=np.round(trend_data["atr"].to_numpy()[-1], 2)
            )
            print('***** BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY *****')

        print('\n')

    stored_trades = [trade for trade in trades_repo.get_all_trades() if trade.id != new_trade_id and not trade.is_closed]

    for trade in stored_trades:
        trade_closed = False
        reason = Reason.NONE
        profit = 0
        current_price = 0

        if trade.date_time >= current_date:
            continue

        if trade.side == Side.BUY or trade.side == Side.SELL:
            if trade.side == Side.BUY:
                if current_low <= trade.stop_loss:
                    reason = Reason.STOP_LOSS
                    profit = round(trade.quantity * (current_low - trade.price), 2)
                    current_price = current_low
                    trade_closed = True
                elif current_high >= trade.take_profit:
                    reason = Reason.TAKE_PROFIT
                    profit = round(trade.quantity * (current_high - trade.price), 2)
                    current_price = current_high
                    trade_closed = True

            if trade.side == Side.SELL:
                if current_high >= trade.stop_loss:
                    reason = Reason.STOP_LOSS
                    profit = round(trade.quantity * (trade.price - current_high), 2)
                    current_price = current_high
                    trade_closed = True
                elif current_low <= trade.take_profit:
                    reason = Reason.TAKE_PROFIT
                    profit = round(trade.quantity * (trade.price - current_low), 2)
                    current_price = current_low
                    trade_closed = True

        if trade_closed:
            trades_repo.update_trade(
                trade.id,
                is_closed=True,
                close_price=current_price,
                close_date_time = current_date,
                quantity=0,  # Trade is fully closed
                profit=trade.profit if trade.profit is not None else 0 + profit
            )

            print(f'ID: {trade.id} price: {current_price} date: {current_date} profit: {profit} ***** {reason.value} *****')


trades_repo.close()

if __name__ == '__main__':
    pass

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
