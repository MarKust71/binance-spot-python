"""
Binance Trade WebSocket API.
"""
import json

from api_websocket import handle_trade_websocket_message
from api_websocket.binance_websocket_base import BinanceWebSocketBase
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL


class BinanceTradeWebSocket(BinanceWebSocketBase):
    """Manages Binance Trade WebSocket connection."""

    def on_message(self, _ws, message) -> None:
        handle_trade_websocket_message(message)

    def subscribe(self):
        if self.ws:
            payload = {
                "method": "SUBSCRIBE",
                "params": [f"{self.symbol}@trade"],
                "id": 1
            }
            self.ws.send(json.dumps(payload))
        else:
            print("\033[91mTRADES\033[0m-> WebSocket not initialized, "
                  "cannot send subscription request.")

    def get_log_prefix(self) -> str:
        return "TRADES"


def ws_trade(url: str, symbol: str) -> None:
    """Function to start BinanceTradeWebSocket."""
    trade_ws = BinanceTradeWebSocket(url, symbol)
    trade_ws.start()


if __name__ == "__main__":
    URL = f"{API_WEBSOCKET_URL}/ws/{TRADE_SYMBOL.lower()}@trade"
    binance_trade_ws = BinanceTradeWebSocket(URL, TRADE_SYMBOL)
    binance_trade_ws.start()
