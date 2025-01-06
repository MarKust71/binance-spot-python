from api import client
import pandas as pd


# Funkcja pobierania danych świecowych
def fetch_candles(symbol, interval, limit=100):
    try:
        candles = client.get_klines(symbol=symbol, interval=interval, limit=limit)

        data_frame = pd.DataFrame(candles, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        data_frame['timestamp'] = pd.to_datetime(data_frame['timestamp'], unit='ms')
        data_frame['close'] = data_frame['close'].astype(float)

        return data_frame

    except Exception as e:
        print(f"Błąd podczas pobierania świec: {e}")

        return None

