# strategy_tester.py
"""
Strategy tester module.
"""


import talib

from constants import TRADE_SYMBOL, KLINE_INTERVAL, \
    TRADE_SIGNAL_SELL, TRADE_SIGNAL_BUY, TRADE_SIGNAL_NONE
from helpers import determine_trend, fetch_candles, get_rsi_signals, get_trade_signal

candles = fetch_candles(symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=500)

for i in range(0, len(candles) - 200 + 1):

    data = candles.iloc[:200 + i]
    trend = determine_trend(candles)

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
        print(data['timestamp'].to_numpy()[-1], 'price:',
              data['close'].to_numpy()[-1], '| RSI:',
              rsi[-1], '| SMA:', sma[-1], '| RSI swing:',
              rsi_signals["swing"], '| RSI signal:', rsi_signals["signal"])


if __name__ == '__main__':
    pass
