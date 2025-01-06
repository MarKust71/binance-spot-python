from helpers import fetch_candles
from helpers.calculate_ema import calculate_ema


def determine_trend(symbol, interval):
    data_frame = fetch_candles(symbol, interval)
    # print('determine_trend first:', data_frame['close'].iloc[0], data_frame['timestamp'].iloc[0])
    # print('determine_trend last:', data_frame['close'].iloc[-1], data_frame['timestamp'].iloc[-1])
    if data_frame is not None:
        data_frame['ema_50'] = calculate_ema(data_frame['close'], 50)
        data_frame['ema_200'] = calculate_ema(data_frame['close'], 200)
        if data_frame['ema_50'].iloc[-1] > data_frame['ema_200'].iloc[-1]:
            return "bullish"  # Trend wzrostowy
        elif data_frame['ema_50'].iloc[-1] < data_frame['ema_200'].iloc[-1]:
            return "bearish"  # Trend spadkowy
    return None
