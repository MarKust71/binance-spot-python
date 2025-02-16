"""
This module provides a function to print trade updates.
"""


from constants import Reason

def print_trade_update(trade_update):
    """Wypisuje informacje o aktualizacji transakcji."""
    trade = trade_update['trade']
    timestamp = trade_update['timestamp']
    price = trade_update['price']
    quantity = trade_update['quantity']
    profit = trade_update['profit']
    reason = trade_update['reason']

    print(
        f'ID: {trade.id} date: {timestamp} price: {price} '
        f'quantity: {trade.rest_quantity \
            if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT} else quantity} '
        f'profit: {profit} ***** {reason.value} *****'
    )


if __name__ == '__main__':
    pass
