"""
This module initializes a WebSocket connection to trace trades.
"""
from api_websocket.binance_trade_websocket import ws_trade
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL


if __name__ == '__main__':
    URL = f"{API_WEBSOCKET_URL}/ws/{TRADE_SYMBOL.lower()}@trade"
    ws_trade(URL, TRADE_SYMBOL)
