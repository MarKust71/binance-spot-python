import mplfinance as mpf

from constants import TRADE_SYMBOL, KLINE_TREND_INTERVAL
from helpers import fetch_candles

trend_candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=500)
trend_candles.set_index('timestamp', inplace=True)

mpf.plot(
    trend_candles,
    type='candle',
    style='charles',
    volume=False,
    title='Trend Candles',
    ylabel='Price',
    # ylabel_lower='Volume'
)

if __name__ == '__main__':
    # print(type(trend_candles.iloc[-1]['open']))
    pass
