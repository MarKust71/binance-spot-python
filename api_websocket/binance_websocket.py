"""
Binance Kline WebSocket API.
"""
import json

from websocket import WebSocketApp

from api_websocket import handle_websocket_message
from api_websocket.binance_websocket_base import BinanceWebSocketBase
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL


class BinanceKlineWebSocket(BinanceWebSocketBase):
    """Manages Binance Kline WebSocket connection."""

    def __init__(self, url: str, symbol: str, interval: str):
        super().__init__(url, symbol)
        self.interval = interval

    def on_message(self, _ws, message) -> None:
        handle_websocket_message(message)

    def subscribe(self):
        payload = {
            "method": "SUBSCRIBE",
            "params": [f"{self.symbol}@kline_{self.interval}"],
            "id": 1
        }
        self.ws.send(json.dumps(payload))

    def create_websocket(self) -> WebSocketApp:
        """Creates a WebSocketApp instance."""
        socket = f"{self.url}/ws/{self.symbol.lower()}@kline_{self.interval}"
        print(f'\033[92mTRADES\033[0m-> socket: {socket}')

        return WebSocketApp(
            socket,
            on_open=self.on_open,
            on_close=self.on_close,
            on_message=self.on_message,
            on_error=self.on_error,
        )

    def get_log_prefix(self) -> str:
        return "KLINES"


def ws_kline(url: str, symbol: str, interval: str) -> WebSocketApp:
    """Function to start BinanceKlineWebSocket."""
    return BinanceKlineWebSocket(url, symbol, interval).create_websocket()

if __name__ == "__main__":
    binance_kline_ws = BinanceKlineWebSocket(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
    binance_kline_ws.run()
