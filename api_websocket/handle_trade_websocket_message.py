# api/handle_trade_websocket_message.py
"""
Binance handle trade websocket message module.
"""


import json
import pandas as pd
# import numpy as np

# from constants import TRADE_SYMBOL, KLINE_INTERVAL, TRADE_VALUE, KLINE_TREND_INTERVAL, TradeSignal, Reason, Side
# from constants import Reason, Side
# from db.repositories import TradeRepository
from db.utils import db_update_trades

# from helpers import fetch_candles, determine_trend, get_trade_signal, set_fractals

LIMIT = 200
TREND_LIMIT = 200
DELAY = 0
FRACTALS_PERIODS = 8

LAST_CLOSE = None

def handle_trade_websocket_message(message) -> None:
    """
    This function handles websocket message.

    Args:
        message: Description of param1.

    Returns:
        None
    """


    json_message = json.loads(message)
    event_time = pd.to_datetime(json_message['E'], unit='ms')
    event_price = pd.to_numeric(json_message['p'])
    symbol = json_message['s']

    # print(
    #     f'event_time: {event_time}, '
    #     f'price: {price}, '
    #     f'symbol: {symbol}'
    # )


    db_update_trades(
        symbol=symbol,
        price=event_price,
        timestamp=event_time
    )

    # trades_repo = TradeRepository()
    #
    # stored_trades = [trade for trade in trades_repo.get_all_trades() if not trade.is_closed]
    #
    # for trade in stored_trades:
    #     trade_closed = False
    #     reason = Reason.NONE
    #     profit = 0
    #
    #     if trade.date_time >= event_time:
    #         continue
    #
    #     if trade.side == Side.BUY or trade.side == Side.SELL:
    #         if trade.side == Side.BUY:
    #             if event_price <= trade.stop_loss:
    #                 reason = Reason.STOP_LOSS
    #                 profit = round(trade.quantity * (event_price - trade.price), 2)
    #                 trade_closed = True
    #             elif event_price >= trade.take_profit:
    #                 reason = Reason.TAKE_PROFIT
    #                 profit = round(trade.quantity * (event_price - trade.price), 2)
    #                 trade_closed = True
    #
    #         if trade.side == Side.SELL:
    #             if event_price >= trade.stop_loss:
    #                 reason = Reason.STOP_LOSS
    #                 profit = round(trade.quantity * (trade.price - event_price), 2)
    #                 trade_closed = True
    #             elif event_price <= trade.take_profit:
    #                 reason = Reason.TAKE_PROFIT
    #                 profit = round(trade.quantity * (trade.price - event_price), 2)
    #                 trade_closed = True
    #
    #     if trade_closed:
    #         trades_repo.update_trade(
    #             trade.id,
    #             is_closed=True,
    #             close_price=event_price,
    #             close_date_time = event_time,
    #             quantity=0,  # Trade is fully closed
    #             profit=trade.profit if trade.profit is not None else 0 + profit
    #         )
    #
    #         print(f'ID: {trade.id} price: {event_price} date: {event_time} profit: {profit} ***** {reason.value} *****')
    #
    #
    # trades_repo.close()
