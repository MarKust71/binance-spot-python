# api/binance_websocket.py
"""
Binance websocket module.
"""


import websocket

from websocket import WebSocketApp
from api.handle_websocket_message import handle_websocket_message


def on_error(ws, error) -> None:
    """
    This function does something.

    Args:
        ws: Description of param1.
        error: Description of param2.

    Returns:
        None
    """
    print('error', error)


def on_open(ws) -> None:
    """
    This function does something.

    Args:
        ws: Description of param1.

    Returns:
        None
    """
    print('connection opened')


def on_close(ws, status_code, close_msg) -> None:
    """
    This function does something.

    Args:
        ws: Description of param1.
        status_code: Description of param1.
        close_msg: Description of param1.

    Returns:
        None
    """
    print(f'connection closed: status code: {status_code}, message: {close_msg}')


def on_message(ws, message) -> None:
    """
    This function does something.

    Args:
        ws: Description of param1.
        message: Description of param1.

    Returns:
        None.
    """
    handle_websocket_message(message)


def ws_kline(url: str, symbol: str, interval: str) -> WebSocketApp:
    """
    This function does something.

    Args:
        url: Description of param1.
        symbol: Description of param1.
        interval: Description of param1.

    Returns:
        None.
    """
    socket = f"{url}/ws/{symbol.lower()}@kline_{interval}"
    print(socket)

    return websocket.WebSocketApp(
        socket, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error
    )
