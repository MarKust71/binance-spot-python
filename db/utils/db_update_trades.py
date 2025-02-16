import pandas as pd

from constants import Reason
from db.repositories import TradeRepository

from .determine_trade_outcome import determine_trade_outcome
from .print_trade_update import print_trade_update


def db_update_trades(symbol: str, price: float, timestamp: pd.Timestamp) -> None:
    trades_repo = TradeRepository()

    for trade in [t for t in trades_repo.get_all_trades() if not t.is_closed]:
        if trade.date_time >= timestamp or trade.symbol != symbol:
            continue

        reason, quantity, profit = determine_trade_outcome(trade, price)

        if reason == Reason.NONE:
            continue

        print_trade_update(trade, timestamp, price, quantity, profit, reason)

        trades_repo.update_trade(
            trade.id,
            is_closed=reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT},
            close_price=price if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT} else trade.close_price,
            close_date_time=timestamp if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT} else trade.close_date_time,
            take_profit_partial_price=price if reason == Reason.TAKE_PROFIT_PARTIAL else trade.take_profit_partial_price,
            take_profit_partial_quantity=quantity if reason == Reason.TAKE_PROFIT_PARTIAL else trade.take_profit_partial_quantity,
            take_profit_partial_date_time=timestamp if reason == Reason.TAKE_PROFIT_PARTIAL else trade.take_profit_partial_date_time,
            rest_quantity=0 if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT} else round(trade.rest_quantity - quantity, 4),
            profit=round(profit + (trade.profit or 0), 2),
        )

    trades_repo.close()
