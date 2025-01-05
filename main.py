import ssl
from api.binance_websocket import ws_connect
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL
from helpers import fetch_candles

# candles = client.get_klines(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100)
# print(candles[-1])
candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100)
print(candles)

ws = ws_connect(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
