"""
Binance Trade WebSocket API.
"""
import json

from websocket import WebSocketApp

from api_websocket import handle_trade_websocket_message
from api_websocket.binance_websocket_base import BinanceWebSocketBase
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL


class BinanceTradeWebSocket(BinanceWebSocketBase):
    """Manages Binance Trade WebSocket connection."""

    def on_message(self, _ws, message) -> None:
        handle_trade_websocket_message(message)

    def subscribe(self):
        payload = {
            "method": "SUBSCRIBE",
            "params": [f"{self.symbol}@trade"],
            "id": 1
        }
        self.ws.send(json.dumps(payload))

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

    def get_log_prefix(self) -> str:
        return "TRADES"


def ws_trade(url: str, symbol: str) -> WebSocketApp:
    """Function to start BinanceTradeWebSocket."""
    return BinanceTradeWebSocket(url, symbol).create_websocket()


if __name__ == "__main__":
    binance_trade_ws = BinanceTradeWebSocket(API_WEBSOCKET_URL, TRADE_SYMBOL)
    binance_trade_ws.run()
