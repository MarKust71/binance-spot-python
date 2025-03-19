"""
This module determines the outcome of a trade based on the given price.
"""
from constants import Reason, Side, TradeStatus, FORCE_TAKE_PROFIT, TRADE_SYMBOL, KLINE_INTERVAL
# from db.repositories.trade_repository import TP_SL
from db.utils.calculate_profit import calculate_profit
from helpers import fetch_candles

LIMIT=20

def determine_trade_outcome(trade, price):
    """Określa wynik transakcji na podstawie ceny."""
    reason, quantity, profit, stop_loss_new = Reason.NONE, 0, 0, 0

    candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, end_time=None
    )
    candle_data = {
        "atr": candles['atr'].to_numpy()[-1],
    }

    # TD: make depend on a param
    # trailing_stop_loss_basis = TP_SL
    trailing_stop_loss_basis = candle_data["atr"]

    is_buy_factor = 1 if trade.side == Side.BUY else -1

    if (price - trade.stop_loss) * is_buy_factor <= 0:
        reason = Reason.STOP_LOSS
        quantity = trade.rest_quantity
        profit = calculate_profit(quantity, price, trade.price, is_buy_factor)
    elif FORCE_TAKE_PROFIT and (price - trade.take_profit) * is_buy_factor >= 0:
        reason = Reason.TAKE_PROFIT
        quantity = trade.rest_quantity
        profit = calculate_profit(quantity, price, trade.price, is_buy_factor)
    elif trade.status == TradeStatus.SAFE:
        if (trade.stop_loss -
            (price - trailing_stop_loss_basis * 2 * is_buy_factor)) * is_buy_factor < 0:
            reason = Reason.UPDATE_STOP_LOSS
            stop_loss_new = round(price - trailing_stop_loss_basis * 2 * is_buy_factor, 2)
    elif ((price - trade.take_profit_safe) * is_buy_factor >= 0
          and trade.take_profit_safe_date_time is None
          and trade.take_profit_partial_date_time is not None):
        reason = Reason.TAKE_PROFIT_SAFE
        quantity = round(trade.rest_quantity / 2, 4)
        profit = calculate_profit(quantity, price, trade.price, is_buy_factor)
    elif ((price - trade.take_profit_partial) * is_buy_factor >= 0
          and trade.take_profit_partial_date_time is None):
        reason = Reason.TAKE_PROFIT_PARTIAL
        quantity = round(trade.quantity / 3, 4)
        profit = calculate_profit(quantity, price, trade.price, is_buy_factor)

    return reason, quantity, profit, stop_loss_new


if __name__ == '__main__':
    pass
