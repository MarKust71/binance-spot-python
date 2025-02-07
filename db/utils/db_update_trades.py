import pandas as pd

from constants import Reason, Side
from db.repositories import TradeRepository


def db_update_trades(
        symbol: str,
        price: float,
        timestamp: pd.Timestamp,
    ) -> None:

    global quantity
    trades_repo = TradeRepository()

    stored_trades = [trade for trade in trades_repo.get_all_trades() if not trade.is_closed]

    for trade in stored_trades:
        trade_closed = False
        trade_updated = False
        reason = Reason.NONE
        profit = 0

        if trade.date_time >= timestamp or trade.symbol != symbol:
            continue

        if trade.side == Side.BUY:
            if price <= trade.stop_loss:
                reason = Reason.STOP_LOSS
                profit = round(trade.quantity * (price - trade.price), 2)
                quantity = 0
                trade_closed = trade_updated = True
            elif price >= trade.take_profit:
                reason = Reason.TAKE_PROFIT
                profit = round(trade.quantity * (price - trade.price), 2)
                quantity = 0
                trade_closed = trade_updated = True
            elif price >= trade.take_profit_partial and trade.take_profit_partial_date_time is None and not trade_closed:
                reason = Reason.TAKE_PROFIT_PARTIAL
                quantity = round(trade.quantity / 3, 4)
                profit = round(quantity * (price - trade.price), 2)
                trade_closed = False
                trade_updated = True

        if trade.side == Side.SELL:
            if price >= trade.stop_loss:
                reason = Reason.STOP_LOSS
                profit = round(trade.quantity * (trade.price - price), 2)
                quantity = 0
                trade_closed = trade_updated = True
            elif price <= trade.take_profit:
                reason = Reason.TAKE_PROFIT
                profit = round(trade.quantity * (trade.price - price), 2)
                quantity = 0
                trade_closed = trade_updated = True
            elif price <= trade.take_profit_partial and trade.take_profit_partial_date_time is None and not trade_closed:
                reason = Reason.TAKE_PROFIT_PARTIAL
                quantity = round(trade.rest_quantity / 3, 4)
                profit = round(quantity * (trade.price - price), 2)
                trade_closed = False
                trade_updated = True

        if trade_updated:
            print(f'ID: {trade.id} date: {timestamp} price: {price} '
                  f'quantity: {trade.rest_quantity if trade_closed else quantity} '
                  f'profit: {profit} ***** {reason.value} *****')

            trades_repo.update_trade(
                trade.id,
                is_closed = True if trade_closed else False,
                close_price = price if trade_closed else trade.close_price,
                close_date_time = timestamp if trade_closed else trade.close_date_time,
                take_profit_partial_price = trade.take_profit_partial_price if trade_closed else price,
                take_profit_partial_quantity = quantity if not trade_closed else trade.take_profit_partial_quantity,
                take_profit_partial_date_time = trade.take_profit_partial_date_time if trade_closed else timestamp,
                rest_quantity = 0 if trade_closed else round(trade.rest_quantity - quantity, 4),  # Trade is fully closed
                profit = round(profit + (trade.profit if trade.profit is not None else 0), 2)
            )


    trades_repo.close()
