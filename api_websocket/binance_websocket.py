# api/binance_websocket.py
"""
Binance websocket module.
"""

import ssl
import json
import websocket

from websocket import WebSocketApp
from api_websocket.handle_websocket_message import handle_websocket_message
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL


def on_error(_ws, error) -> None:
    """
    Handle WebSocket errors.

    Args:
        _ws: WebSocket instance.
        error: Error message.

    Returns:
        None
    """
    print('KLINES-> error', error)


def on_open(_ws) -> None:
    """
    Handle WebSocket opening.

    Args:
        _ws: WebSocket instance.

    Returns:
        None
    """
    print('KLINES-> connection opened')


def on_close(_ws, status_code, close_msg) -> None:
    """
    Handle WebSocket closure.

    Args:
        _ws: WebSocket instance.
        status_code: Status code of closure.
        close_msg: Message associated with closure.

    Returns:
        None
    """
    print(f'KLINES-> connection closed: status code: {status_code}, message: {close_msg}')


def on_message(ws, message) -> None:
    """
    Handle WebSocket messages.

    Args:
        ws: WebSocket instance.
        message: Message received.

    Returns:
        None.
    """
    try:
        data = json.loads(message)

        # Check if it's a ping message
        if "ping" in data:
            print("\033[93mKLINES\033[0m-> received ping, sending pong")
            ws.send(json.dumps({"pong": data["ping"]}))  # Send a pong response
            return

        handle_websocket_message(message)

    except json.JSONDecodeError:
        print("KLINES-> Received non-JSON message:", message)


def ws_kline(url: str, symbol: str, interval: str) -> WebSocketApp:
    """
    Create a WebSocket connection to Binance for kline data.

    Args:
        url: Binance WebSocket API URL.
        symbol: Trading pair symbol.
        interval: Kline interval.

    Returns:
        WebSocketApp instance.
    """
    socket = f"{url}/ws/{symbol.lower()}@kline_{interval}"
    print(f'KLINES-> socket: {socket}')

    return websocket.WebSocketApp(
        socket, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error
    )


if __name__ == '__main__':
    websocket = ws_kline(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
    websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
