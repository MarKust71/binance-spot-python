# api/binance_trade_websocket.py
"""
Binance websocket module.
"""

import ssl
import websocket

from websocket import WebSocketApp
from api_websocket import handle_trade_websocket_message
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL


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
    handle_trade_websocket_message(message)


def ws_trade(url: str, symbol: str) -> WebSocketApp:
    """
    This function does something.

    Args:
        url: Description of param1.
        symbol: Description of param1.

    Returns:
        None.
    """
    socket = f"{url}/ws/{symbol.lower()}@trade"
    print(socket)

    return websocket.WebSocketApp(
        socket, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error
    )


if __name__ == '__main__':
    ws = ws_trade(API_WEBSOCKET_URL, TRADE_SYMBOL)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
