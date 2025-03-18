# api/handle_trade_websocket_message.py
"""
Binance handle trade websocket message module.
"""
import json
import pandas as pd

from db.utils import db_update_trades


def handle_trade_websocket_message(message) -> None:
    """
    This function handles trade websocket message.

    Args:
        message: Description of param1.

    Returns:
        None
    """
    json_message = json.loads(message)
    event_time = pd.to_datetime(json_message['E'], unit='ms')
    event_price = pd.to_numeric(json_message['p'])
    symbol = json_message['s']

    db_update_trades(
        symbol=symbol,
        price=event_price,
        timestamp=event_time
    )
