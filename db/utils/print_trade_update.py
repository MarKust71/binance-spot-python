from constants import Reason


def print_trade_update(trade, timestamp, price, quantity, profit, reason):
    """Wypisuje informacje o aktualizacji transakcji."""
    print(
        f'ID: {trade.id} date: {timestamp} price: {price} '
        f'quantity: {trade.rest_quantity if reason in {Reason.STOP_LOSS, Reason.TAKE_PROFIT} else quantity} '
        f'profit: {profit} ***** {reason.value} *****'
    )


if __name__ == '__main__':
    pass
