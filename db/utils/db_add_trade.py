# db_add_trade.py
"""
Adds trade into database if conditions met.
"""
import pandas as pd
import numpy as np
import websocket

from constants import TradeSignal, TRADE_VALUE, TRADE_SYMBOL, Side, Reason
from db.repositories import TradeRepository, TradeData
from db.utils.serialize_data import serialize_data
from helpers import set_fractals, determine_trend, get_trade_signal


def db_add_trade(
    candles: pd.DataFrame,
    trend_candles: pd.DataFrame,
    delay: int,
    fractals_periods: int,
) -> int | None:
    """
    Add a new trade to the database.

    Args:
        candles: Candles dataframe.
        trend_candles: Trend candles dataframe.
        delay: Delay.
        fractals_periods: Fractals periods.
    """
    trend_data = trend_candles[
        trend_candles['timestamp']
        <= candles['timestamp'].iloc[-1] - pd.Timedelta(minutes=delay * fractals_periods)
        ]
    trend_data=set_fractals(trend_data, periods=fractals_periods)
    last_fractals = trend_data[
        trend_data['Fractal_Up'].notnull()
        | trend_data['Fractal_Down'].notnull()
        ][['timestamp', 'Fractal_Down', 'Fractal_Up']].tail(4)

    trend = determine_trend(trend_data.iloc[:-fractals_periods], candles.iloc[-1])

    trade_signal = get_trade_signal(trend, candles, fractals=last_fractals)

    if trade_signal != TradeSignal.NONE:
        quantity=round(TRADE_VALUE / candles["close"].to_numpy()[-1], 4)

        print(f'ATR: {trend_data["atr"].iloc[-1]:,.2f}')
        print(f'QTY: {quantity}')

        trades_repo = TradeRepository()
        trade_data_row = {
            'date_time': candles['timestamp'].iloc[-1],
            'symbol': TRADE_SYMBOL,
            'side': Side.SELL if trade_signal == TradeSignal.SELL else Side.BUY,
            'price': candles["close"].to_numpy()[-1],
            'quantity': quantity,
            'atr': np.round(trend_data["atr"].to_numpy()[-1], 2),
            'reason': Reason.NONE,
        }
        trade_data = TradeData(
            date_time=trade_data_row['date_time'],
            symbol=trade_data_row['symbol'],
            side=trade_data_row['side'],
            price=trade_data_row['price'],
            quantity=trade_data_row['quantity'],
            atr=trade_data_row['atr']
        )
        new_trade_id = trades_repo.add_trade(trade_data)
        trades_repo.close()

        # Wysyłanie komunikatu WebSocket
        try:
            ws = websocket.create_connection("ws://127.0.0.1:8000/ws")
            ws.send(serialize_data(trade_data_row))
            ws.close()
        except ConnectionRefusedError:
            print('New trade: WebSocket server is not running')

        if trade_signal == TradeSignal.SELL:
            print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')

        if trade_signal == TradeSignal.BUY:
            print('***** BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY *****')


        #
        #     order_succeeded = create_order(
        #         side=trade_signal,
        #         quantity=quantity,
        #         symbol=TRADE_SYMBOL
        #     )
        #

        return new_trade_id

    return -1
