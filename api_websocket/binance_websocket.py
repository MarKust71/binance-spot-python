# api/binance_websocket.py
"""
Binance websocket module.
"""

import ssl
import websocket

from websocket import WebSocketApp
from api_websocket.handle_websocket_message import handle_websocket_message
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL


def on_error(_ws, error) -> None:
    """
    This function does something.

    Args:
        _ws: Description of param1.
        error: Description of param2.

    Returns:
        None
    """
    print('KLINES-> error', error)


def on_open(_ws) -> None:
    """
    This function does something.

    Args:
        _ws: Description of param1.

    Returns:
        None
    """
    print('KLINES-> connection opened')


def on_close(_ws, status_code, close_msg) -> None:
    """
    This function does something.

    Args:
        _ws: Description of param1.
        status_code: Description of param1.
        close_msg: Description of param1.

    Returns:
        None
    """
    print(f'KLINES-> connection closed: status code: {status_code}, message: {close_msg}')


def on_message(_ws, message) -> None:
    """
    This function does something.

    Args:
        _ws: Description of param1.
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
    print(f'KLINES-> socket: {socket}')

    return websocket.WebSocketApp(
        socket, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error
    )


if __name__ == '__main__':
    websocket = ws_kline(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
    websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
