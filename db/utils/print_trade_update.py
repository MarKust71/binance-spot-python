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

    color = "\033[92m" if profit > 0 else "\033[91m" if profit < 0 else ""
    reset_color = "\033[0m" if color else ""

    print(
        f'ID: {trade.id} date: {timestamp} price: {price} '
        f'quantity: {trade.rest_quantity \
            if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT} else quantity} '
        f'profit: {profit} {color}***** {reason.value} *****{reset_color}'
    )


if __name__ == '__main__':
    pass
