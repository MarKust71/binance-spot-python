"""
This module provides functions to fetch candlestick data from a financial API and process it.
"""


from datetime import datetime
import ta
import pandas as pd
from api import client


# Funkcja pobierania danych świecowych
def fetch_candles(symbol, interval, limit, end_time) -> pd.DataFrame:
    """
    This function does something.

    Args:
        symbol: Description of param1.
        interval: Description of param1.
        limit: Description of param1.
        end_time: Description of param1.

    Returns:
        Data frame with candles
    """
    try:
        candles = client.get_klines(symbol=symbol, interval=interval, limit=limit, endTime=end_time)

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

        # talib
        # data_frame['atr'] = talib.ATR(data_frame['high'].to_numpy(), data_frame['low'].to_numpy(),
        #                               data_frame['close'].to_numpy(), timeperiod=14)
        # data_frame['rsi'] = talib.RSI(data_frame['close'].to_numpy(), timeperiod=14)
        # data_frame['sma'] = talib.SMA(data_frame['rsi'].to_numpy(), timeperiod=14)

        # pandas_ta
        # data_frame['atr'] = ta.atr(data_frame['high'].to_numpy(), data_frame['low'].to_numpy(),
        #                               data_frame['close'].to_numpy(), length=14)
        # data_frame['rsi'] = ta.rsi(data_frame['close'].to_numpy(), length=14)
        # data_frame['sma'] = ta.sma(data_frame['rsi'].to_numpy(), length=14)

        # ta
        data_frame['atr'] = ta.wrapper.AverageTrueRange(data_frame['high'], data_frame['low'],
                                      data_frame['close'], window=14).average_true_range()
        data_frame['rsi'] = ta.wrapper.RSIIndicator(data_frame['close'], window=14).rsi()
        data_frame['sma'] = ta.wrapper.SMAIndicator(data_frame['rsi'], window=14).sma_indicator()

        return data_frame

    except (ValueError, KeyError, TypeError, Exception) as e:
        print(f"Błąd podczas pobierania świec: {e}")

        return pd.DataFrame()


if __name__ == '__main__':
    DATE_STRING = '2025-01-25 12:00:59.999000'
    date_object = datetime.strptime(DATE_STRING, '%Y-%m-%d %H:%M:%S.%f')
    timestamp = int(date_object.timestamp() * 1000)
    print(timestamp)

    try:
        df = fetch_candles('ETHUSDT', '5m', 30, end_time=timestamp)

        if not df.empty:
            # Zapisywanie danych do pliku CSV
            df.to_csv('ohlc_data.csv', index=False)
            print("Dane zostały zapisane jako 'ohlc_data.csv'.")
        else:
            print("Nie udało się pobrać danych.")

    except (ValueError, KeyError, TypeError) as e:
        print(f"Błąd podczas pobierania świec: {e}")
