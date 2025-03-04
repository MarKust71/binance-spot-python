"""
This module initializes a WebSocket connection to trace trades.
"""


import ssl

from api_websocket import ws_trade
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL


if __name__ == '__main__':
    URL = f"{API_WEBSOCKET_URL}/ws/{TRADE_SYMBOL.lower()}@trade"
    ws = ws_trade(URL, TRADE_SYMBOL)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
