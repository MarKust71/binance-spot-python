"""
Binance Kline WebSocket API.
"""
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
        pass

    def get_log_prefix(self) -> str:
        return "KLINES"


def ws_kline(url: str, symbol: str, interval: str) -> None:
    """Function to start BinanceKlineWebSocket."""
    kline_ws = BinanceKlineWebSocket(url, symbol, interval)
    kline_ws.start()


if __name__ == "__main__":
    URL = f"{API_WEBSOCKET_URL}/ws/{TRADE_SYMBOL.lower()}@kline_{KLINE_INTERVAL}"
    binance_kline_ws = BinanceKlineWebSocket(URL, TRADE_SYMBOL, KLINE_INTERVAL)
    binance_kline_ws.start()
