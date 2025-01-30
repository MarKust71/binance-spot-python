# helpers/determine_trend.py
from datetime import datetime

import pandas as pd
import talib

from api import client


# Funkcja pobierania danych świecowych
def fetch_candles(symbol, interval, limit, endTime) -> pd.DataFrame:
    """
    This function does something.

    Args:
        symbol: Description of param1.
        interval: Description of param1.
        limit: Description of param1.
        endTime: Description of param1.

    Returns:
        Data frame with candles
    """
    try:
        candles = client.get_klines(symbol=symbol, interval=interval, limit=limit, endTime=endTime)

        data_frame = pd.DataFrame(candles, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        data_frame['timestamp'] = pd.to_datetime(data_frame['timestamp'], unit='ms')
        data_frame['close_time'] = pd.to_datetime(data_frame['close_time'], unit='ms')
        data_frame['open'] = data_frame['open'].astype(float)
        data_frame['high'] = data_frame['high'].astype(float)
        data_frame['low'] = data_frame['low'].astype(float)
        data_frame['close'] = data_frame['close'].astype(float)
        data_frame['volume'] = data_frame['volume'].astype(float)

        data_frame['atr'] = talib.ATR(data_frame['high'].to_numpy(), data_frame['low'].to_numpy(),
                                      data_frame['close'].to_numpy(), timeperiod=14)
        data_frame['rsi'] = talib.RSI(data_frame['close'].to_numpy(), timeperiod=14)
        data_frame['sma'] = talib.SMA(data_frame['rsi'].to_numpy(), timeperiod=14)

        return data_frame

    except Exception as e:
        print(f"Błąd podczas pobierania świec: {e}")

        return pd.DataFrame()


if __name__ == '__main__':
    pass
    date_string = '2025-01-25 12:00:59.999000'
    date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    timestamp = int(date_object.timestamp() * 1000)
    print(timestamp)

    try:
        df = fetch_candles('ETHUSDT', '5m', 10, endTime=timestamp)

        if not df.empty:
            # Zapisywanie danych do pliku CSV
            df.to_csv('ohlc_data.csv', index=False)
            print("Dane zostały zapisane jako 'ohlc_data.csv'.")
        else:
            print("Nie udało się pobrać danych.")

    except Exception as e:
        print(f"Błąd podczas pobierania świec: {e}")
