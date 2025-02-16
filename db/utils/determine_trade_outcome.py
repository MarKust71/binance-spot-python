from constants import Reason, Side


def determine_trade_outcome(trade, price):
    """Określa wynik transakcji na podstawie ceny."""
    reason, quantity, profit = Reason.NONE, 0, 0

    if trade.side == Side.BUY:
        if price <= trade.stop_loss:
            reason = Reason.STOP_LOSS
            profit = round(trade.quantity * (price - trade.price), 2)
        elif price >= trade.take_profit:
            reason = Reason.TAKE_PROFIT
            profit = round(trade.quantity * (price - trade.price), 2)
        elif price >= trade.take_profit_partial and trade.take_profit_partial_date_time is None:
            reason = Reason.TAKE_PROFIT_PARTIAL
            quantity = round(trade.quantity / 3, 4)
            profit = round(quantity * (price - trade.price), 2)

    elif trade.side == Side.SELL:
        if price >= trade.stop_loss:
            reason = Reason.STOP_LOSS
            profit = round(trade.quantity * (trade.price - price), 2)
        elif price <= trade.take_profit:
            reason = Reason.TAKE_PROFIT
            profit = round(trade.quantity * (trade.price - price), 2)
        elif price <= trade.take_profit_partial and trade.take_profit_partial_date_time is None:
            reason = Reason.TAKE_PROFIT_PARTIAL
            quantity = round(trade.rest_quantity / 3, 4)
            profit = round(quantity * (trade.price - price), 2)

    return reason, quantity, profit


if __name__ == '__main__':
    pass
