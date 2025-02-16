"""
This module initializes a WebSocket connection to trace klines.
"""


import ssl

from api_websocket import ws_kline
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL


if __name__ == '__main__':
    ws = ws_kline(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
