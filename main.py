# main.py
"""
Main module.
"""


import ssl

from api_websocket import ws_kline
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL #, KLINE_TREND_INTERVAL

ws = ws_kline(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == '__main__':
    pass
