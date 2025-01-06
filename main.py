import ssl, talib

# from binance import KLINE_INTERVAL_5MINUTE
from api.binance_websocket import ws_connect
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL, KLINE_TREND_INTERVAL
from helpers import fetch_candles, determine_trend

# candles = client.get_klines(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100)
# print(candles[-1])
candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=100)
# print('first:', candles['close'].iloc[0], candles['timestamp'].iloc[0])
# print('last:', candles['close'].iloc[-1], candles['timestamp'].iloc[-1])
timestamp = candles['timestamp'].to_numpy()[-1]
rsi = talib.RSI(candles['close'].to_numpy())
sma = talib.SMA(rsi, timeperiod=14)
print(timestamp, '| RSI:', rsi[-1], '| SMA:', sma[-1])

# data_frame = fetch_candles(symbol=TRADE_SYMBOL, interval=KLONE_TREND_INTERVAL, limit=100)
# trend = determine_trend(TRADE_SYMBOL, data_frame)
trend = determine_trend(TRADE_SYMBOL, KLINE_TREND_INTERVAL)
print('determine_trend:', trend.upper())

ws = ws_connect(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
