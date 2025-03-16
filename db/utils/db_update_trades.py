"""
This module updates trades in the database based on the given symbol, price, and timestamp.
"""
import pandas as pd

from constants import Reason, TradeStatus
from db.repositories import TradeRepository
from utils.send_websocket_message import send_websocket_message

from .determine_trade_outcome import determine_trade_outcome
from .print_trade_update import print_trade_update


def db_update_trades(symbol: str, price: float, timestamp: pd.Timestamp) -> None:
    """
    Updates trades in the database based on the given symbol, price, and timestamp.

    Args:
        symbol (str): The symbol of the trade.
        price (float): The price of the trade.
        timestamp (pd.Timestamp): The timestamp of the trade.
    """
    trades_repo = TradeRepository()

    for trade in trades_repo.get_trades_by_symbol_older_than_timestamp(
        symbol=symbol,
        time_from=timestamp,
        is_closed=False
    ):
        reason, quantity, profit, stop_loss_new = determine_trade_outcome(trade, price)

        if reason == Reason.NONE:
            continue

        trade_update = {
            'trade': trade,
            'timestamp': timestamp,
            'price': price,
            'quantity': quantity,
            'profit': profit,
            'reason': reason,
            'stop_loss': stop_loss_new
        }
        print_trade_update(trade_update)

        # Wysyłanie komunikatu WebSocket
        send_websocket_message(
            message_data=trade_update,
            error_message="Update trade: WebSocket server is not running"
        )

        trades_repo.update_trade(
            trade.id,
            is_closed=reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT},
            status=TradeStatus.CLOSED if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT}
                else TradeStatus.SAFE if reason == Reason.TAKE_PROFIT_SAFE
                else TradeStatus.PARTIAL if reason == Reason.TAKE_PROFIT_PARTIAL
                else trade.status,

            close_price=price if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT}
                else trade.close_price,
            close_date_time=timestamp if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT}
                else trade.close_date_time,

            take_profit_safe_price=price if reason == Reason.TAKE_PROFIT_SAFE
                else trade.take_profit_safe_price,
            take_profit_safe_quantity=quantity if reason == Reason.TAKE_PROFIT_SAFE
                else trade.take_profit_safe_quantity,
            take_profit_safe_date_time=timestamp if reason == Reason.TAKE_PROFIT_SAFE
                else trade.take_profit_safe_date_time,

            stop_loss=stop_loss_new if reason == Reason.UPDATE_STOP_LOSS
                else trade.stop_loss,

            take_profit_partial_price=price if reason == Reason.TAKE_PROFIT_PARTIAL
                else trade.take_profit_partial_price,
            take_profit_partial_quantity=quantity if reason == Reason.TAKE_PROFIT_PARTIAL
                else trade.take_profit_partial_quantity,
            take_profit_partial_date_time=timestamp if reason == Reason.TAKE_PROFIT_PARTIAL
                else trade.take_profit_partial_date_time,

            rest_quantity=0 if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT}
                else round(trade.rest_quantity - quantity, 4),

            profit=round(profit + (trade.profit or 0), 2),
        )

    trades_repo.close()
