from helpers import fetch_candles
from helpers.calculate_ema import calculate_ema


def determine_trend(symbol, interval):
    data_frame = fetch_candles(symbol, interval)

    if data_frame is not None:
        data_frame['ema_50'] = calculate_ema(data_frame['close'], 50)
        data_frame['ema_200'] = calculate_ema(data_frame['close'], 200)
        if data_frame['ema_50'].iloc[-1] > data_frame['ema_200'].iloc[-1]:
            return "bullish"  # Trend wzrostowy
        elif data_frame['ema_50'].iloc[-1] < data_frame['ema_200'].iloc[-1]:
            return "bearish"  # Trend spadkowy
    return None