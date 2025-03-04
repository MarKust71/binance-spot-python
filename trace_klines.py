"""
This module initializes a WebSocket connection to trace klines.
"""
from api_websocket.binance_websocket import ws_kline
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL


if __name__ == '__main__':
    URL = f"{API_WEBSOCKET_URL}/ws/{TRADE_SYMBOL.lower()}@kline_{KLINE_INTERVAL}"
    ws_kline(URL, TRADE_SYMBOL, KLINE_INTERVAL)
