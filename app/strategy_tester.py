# strategy_tester.py
"""
Strategy tester module.
"""


import talib

from constants import TRADE_SYMBOL, KLINE_INTERVAL, \
    TRADE_SIGNAL_SELL, TRADE_SIGNAL_BUY, TRADE_SIGNAL_NONE, KLINE_TREND_INTERVAL
from helpers import determine_trend, fetch_candles, get_rsi_signals, get_trade_signal
from helpers.calculate_ema import calculate_ema

candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=500)
trend_candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=500)

for i in range(0, len(candles) - 200 + 1):

    trend_data = trend_candles.iloc[:200 + i]
    trend = determine_trend(trend_data)

    data = candles.iloc[:200 + i]

    rsi = talib.RSI(data['close'].to_numpy())
    sma = talib.SMA(rsi, timeperiod=14)

    candle = {
        "timestamp": data['timestamp'].to_numpy()[-2],
        "close": data['close'].to_numpy()[-2],
        "rsi": rsi[-2],
        "sma": sma[-2]
    }

    rsi_signals = get_rsi_signals(rsi)

    trade_signal = get_trade_signal(rsi_signals, trend, data, rsi, sma, candle)

    if trade_signal != TRADE_SIGNAL_NONE:
        if trade_signal == TRADE_SIGNAL_SELL:
            print('***** SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL SELL *****')

        if trade_signal == TRADE_SIGNAL_BUY:
            print('***** BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY BUY *****')

        print('\n')

    else:
        print(data['timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S'), f'| price: {data['close'].to_numpy()[-1]:,.2f}',
              f'| RSI: {rsi[-1]:,.2f}',
              f'| SMA: {sma[-1]:,.2f}', '| RSI swing:',
              rsi_signals["swing"], '| RSI signal:', rsi_signals["signal"],
              '| Trend:', trend.upper(),
              f'| EMA50: {calculate_ema(trend_data['close'], 50).iloc[-1]:,.2f}',
              f'| EMA200: {calculate_ema(trend_data['close'], 200).iloc[-1]:,.2f}')


if __name__ == '__main__':
    pass
