"""
This module provides a function to print trade updates.
"""
import pandas as pd
import pytz

from constants import Reason

def print_trade_update(trade_update):
    """Wypisuje informacje o aktualizacji transakcji."""
    local_tz = pytz.timezone('Europe/Warsaw')

    trade = trade_update['trade']
    timestamp = trade_update['timestamp']
    price = trade_update['price']
    quantity = trade_update['quantity']
    profit = trade_update['profit']
    reason = trade_update['reason']
    stop_loss = trade_update['stop_loss']

    color = "\033[92m" if profit > 0 else "\033[91m" if profit < 0 else ""
    reset_color = "\033[0m" if color else ""

    print(
        f'ID: {trade.id} '
        f'date: {pd.to_datetime(timestamp, unit='ms', utc=True)
            .tz_convert(local_tz).round("min").strftime('%Y-%m-%d %H:%M:%S')} '
        f'price: {price} '
        f'quantity: {trade.rest_quantity \
            if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT} else quantity} '
        f'profit: {profit} S/L: {stop_loss} {color}***** {reason.value} *****{reset_color}'
    )


if __name__ == '__main__':
    pass
