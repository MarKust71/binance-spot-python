"""
This module initializes a WebSocket connection to trace trades.
"""


import ssl

from api_websocket import ws_trade
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL


if __name__ == '__main__':
    ws = ws_trade(API_WEBSOCKET_URL, TRADE_SYMBOL)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
