import pandas as pd

from constants import Reason, Side
from db.repositories import TradeRepository


def db_update_trades(
        symbol: str,
        price: float,
        timestamp: pd.Timestamp,
    ) -> None:

    trades_repo = TradeRepository()

    stored_trades = [trade for trade in trades_repo.get_all_trades() if not trade.is_closed]

    for trade in stored_trades:
        trade_closed = False
        reason = Reason.NONE
        profit = 0

        if trade.date_time >= timestamp or trade.symbol != symbol:
            continue

        if trade.side == Side.BUY or trade.side == Side.SELL:
            if trade.side == Side.BUY:
                if price <= trade.stop_loss:
                    reason = Reason.STOP_LOSS
                    profit = round(trade.quantity * (price - trade.price), 2)
                    trade_closed = True
                elif price >= trade.take_profit:
                    reason = Reason.TAKE_PROFIT
                    profit = round(trade.quantity * (price - trade.price), 2)
                    trade_closed = True

            if trade.side == Side.SELL:
                if price >= trade.stop_loss:
                    reason = Reason.STOP_LOSS
                    profit = round(trade.quantity * (trade.price - price), 2)
                    trade_closed = True
                elif price <= trade.take_profit:
                    reason = Reason.TAKE_PROFIT
                    profit = round(trade.quantity * (trade.price - price), 2)
                    trade_closed = True

        if trade_closed:
            trades_repo.update_trade(
                trade.id,
                is_closed=True,
                close_price=price,
                close_date_time = timestamp,
                quantity=0,  # Trade is fully closed
                profit=trade.profit if trade.profit is not None else 0 + profit
            )

            print(f'ID: {trade.id} price: {price} date: {timestamp} profit: {profit} ***** {reason.value} *****')


    trades_repo.close()
