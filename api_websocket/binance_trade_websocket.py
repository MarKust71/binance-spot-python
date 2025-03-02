"""
Binance websocket module.
"""

import ssl
import time
from datetime import datetime
from websocket import WebSocketApp
from api_websocket.handle_trade_websocket_message import handle_trade_websocket_message
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL


class BinanceWebSocket:
    """Class to manage Binance WebSocket connection."""

    def __init__(self, url: str, symbol: str):
        self.url = url
        self.symbol = symbol
        self.last_open_time = None
        self.ws = None

    def on_error(self, _ws, error) -> None:
        """Handles WebSocket errors."""
        print(f'\033[91mTRADES\033[0m-> error {error}')

    def on_open(self, _ws) -> None:
        """Handles WebSocket opening."""
        self.last_open_time = time.time()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\033[92mTRADES\033[0m-> connection opened at {timestamp}')

    def on_close(self, _ws, status_code, close_msg) -> None:
        """Handles WebSocket closure."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\033[94mTRADES\033[0m-> connection closed at {timestamp}: '
              f'status code: {status_code}, message: {close_msg}')

        if self.last_open_time and (time.time() - self.last_open_time) >= 5:
            print("\033[93mTRADES\033[0m-> Reconnecting WebSocket...")
            self.reconnect()

    def on_message(self, _ws, message) -> None:
        """Handles WebSocket messages."""
        handle_trade_websocket_message(message)

    def create_websocket(self) -> WebSocketApp:
        """Creates a WebSocketApp instance."""
        socket = f"{self.url}/ws/{self.symbol.lower()}@trade"
        print(f'\033[92mTRADES\033[0m-> socket: {socket}')

        return WebSocketApp(
            socket,
            on_open=self.on_open,
            on_close=self.on_close,
            on_message=self.on_message,
            on_error=self.on_error,
        )

    def run(self):
        """Starts the WebSocket connection."""
        self.ws = self.create_websocket()
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def reconnect(self):
        """Reconnects WebSocket."""
        self.last_open_time = time.time()
        self.run()


def ws_trade(url: str, symbol: str) -> WebSocketApp:
    """
    Creates and returns a WebSocketApp instance, maintaining compatibility with previous imports.

    Args:
        url: WebSocket API base URL.
        symbol: Trading pair symbol.

    Returns:
        WebSocketApp instance.
    """
    return BinanceWebSocket(url, symbol).create_websocket()


if __name__ == '__main__':
    binance_ws = BinanceWebSocket(API_WEBSOCKET_URL, TRADE_SYMBOL)
    binance_ws.run()
