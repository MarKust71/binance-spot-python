"""
Binance websocket module.
"""

import ssl
import time
# import websocket

from datetime import datetime

from websocket import WebSocketApp
from api_websocket.handle_trade_websocket_message import handle_trade_websocket_message
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL

last_open_time = 0  # Przechowuje czas ostatniego otwarcia połączenia
ws = None  # Globalna zmienna dla WebSocketApp


def on_error(_ws, error) -> None:
    """
    Handles WebSocket errors.

    Args:
        _ws: WebSocket instance.
        error: Error message.

    Returns:
        None
    """
    print('TRADES-> error', error)


def on_open(_ws) -> None:
    """
    Handles WebSocket opening.

    Args:
        _ws: WebSocket instance.

    Returns:
        None
    """
    global last_open_time
    last_open_time = time.time()  # Zapisujemy czas otwarcia połączenia
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'TRADES-> connection opened at {timestamp}')


def on_close(_ws, status_code, close_msg) -> None:
    """
    Handles WebSocket closure.

    Args:
        _ws: WebSocket instance.
        status_code: Closure status code.
        close_msg: Closure message.

    Returns:
        None
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'TRADES-> connection closed at {timestamp}: status code: {status_code}, '
          f'message: {close_msg}')

    # Sprawdzamy, czy minęło co najmniej 5 sekund od ostatniego otwarcia
    if last_open_time and (time.time() - last_open_time) >= 5:
        print("TRADES-> Reconnecting WebSocket...")
        reconnect()


def on_message(_ws, message) -> None:
    """
    Handles WebSocket messages.

    Args:
        _ws: WebSocket instance.
        message: Incoming message.

    Returns:
        None.
    """
    handle_trade_websocket_message(message)


def ws_trade(url: str, symbol: str) -> WebSocketApp:
    """
    Creates and returns a WebSocketApp instance.

    Args:
        url: WebSocket API base URL.
        symbol: Trading pair symbol.

    Returns:
        WebSocketApp instance.
    """
    socket = f"{url}/ws/{symbol.lower()}@trade"
    print(f'TRADES-> socket: {socket}')

    return WebSocketApp(
        socket, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error
    )


def reconnect():
    """
    Reconnects WebSocket.
    """
    global ws
    ws = ws_trade(API_WEBSOCKET_URL, TRADE_SYMBOL)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == '__main__':
    ws = ws_trade(API_WEBSOCKET_URL, TRADE_SYMBOL)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
