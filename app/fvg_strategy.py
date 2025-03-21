"""
Strategia FVG (Falling Volume Growth)
"""
import pandas as pd
# from binance.client import Client
import matplotlib.pyplot as plt

from api import client


class FVGStrategy:
    """
    Strategia FVG (Falling Volume Growth)
    """
    def __init__(self, symbol='ETHUSDT', interval='1m', limit=200):
        """
        Inicjalizacja strategii
        :param symbol:
        :param interval:
        :param limit:
        """
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        # self.client = Client()
        self.client = client
        self.df = None
        self.fvg_zones = pd.DataFrame()
        self.backtest_results = []


    def get_data(self):
        """
        Pobranie danych z Binance
        :return:
        """
        klines = self.client.get_klines(
            symbol=self.symbol,
            interval=self.interval,
            limit=self.limit
        )
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'num_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df[['open', 'high', 'low', 'close']].astype(float)
        self.df = df


    def detect_fvg(self):
        """
        Wykrywanie strefy FVG
        :return:
        """
        df = self.df
        fvg_list = []
        for i in range(2, len(df)):
            low_a = df.iloc[i - 2]['high']
            high_a = df.iloc[i - 2]['high']
            low_b = df.iloc[i - 1]['low']
            high_b = df.iloc[i - 1]['high']
            low_c = df.iloc[i]['low']
            high_c = df.iloc[i]['low']

            if high_a < low_c and  low_c < high_b and high_a > low_b:
                fvg_list.append({
                    'index': df.index[i],
                    'type': 'bullish',
                    'from': high_a,
                    'to': low_c,
                    'detected_at': df.index[i]
                })

            if high_c < low_a and low_b < high_c and high_b > low_a:
                fvg_list.append({
                    'index': df.index[i],
                    'type': 'bullish',
                    'from': high_a,
                    'to': low_c,
                    'detected_at': df.index[i]
                })
        self.fvg_zones = pd.DataFrame(fvg_list)


    def check_price_return(self):
        """
        Sprawdzenie czy cena wróciła do strefy FVG
        :return:
        """
        if self.fvg_zones.empty or self.df is None:
            return None

        latest = self.df.iloc[-1]
        signals = []

        for _, fvg in self.fvg_zones.iterrows():
            if fvg['type'] == 'bullish':
                if fvg['from'] <= latest['low'] <= fvg['to']:
                    signals.append({
                        'timestamp': self.df.index[-1],
                        'signal': 'BUY',
                        'price': latest['close'],
                        'fvg_from': fvg['from'],
                        'fvg_to': fvg['to'],
                        'fvg_detected_at': fvg['detected_at']
                    })

            if fvg['type'] == 'bearish':
                if fvg['from'] >= latest['high'] >= fvg['to']:
                    signals.append({
                        'timestamp': self.df.index[-1],
                        'signal': 'SELL',
                        'price': latest['close'],
                        'fvg_from': fvg['from'],
                        'fvg_to': fvg['to'],
                        'fvg_detected_at': fvg['detected_at']
                    })

        return signals


    def backtest(self, take_profit=0.0003, stop_loss=0.0001):
        """
        Backtest strategii
        :param take_profit:
        :param stop_loss:
        :return:
        """
        df = self.df
        self.detect_fvg()
        trades = []

        for _, fvg in self.fvg_zones.iterrows():
            entry_index = df.index.get_loc(fvg['index']) + 1
            if entry_index >= len(df):
                continue

            entry_price = df.iloc[entry_index]['close']
            tp_price = entry_price * (1 + take_profit)
            sl_price = entry_price * (1 - stop_loss)

            for i in range(entry_index + 1, len(df)):
                high = df.iloc[i]['high']
                low = df.iloc[i]['low']

                if high >= tp_price:
                    trades.append({
                        'entry_time': df.index[entry_index],
                        'exit_time': df.index[i],
                        'result': 'TP',
                        'entry_price': entry_price,
                        'exit_price': tp_price})
                    break
                if low <= sl_price:
                    trades.append({
                        'entry_time': df.index[entry_index],
                        'exit_time': df.index[i],
                        'result': 'SL',
                        'entry_price': entry_price,
                        'exit_price': sl_price})
                    break
            else:
                trades.append({
                    'entry_time': df.index[entry_index],
                    'exit_time': df.index[-1],
                    'result': 'Open',
                    'entry_price': entry_price,
                    'exit_price': df.iloc[-1]['close']})

        self.backtest_results = trades
        return trades


    def summarize_backtest(self):
        """
        Podsumowanie wyników backtestu
        :return:
        """
        results = self.backtest_results
        if not results:
            print("Brak wyników do podsumowania.")
            return

        tp = [r for r in results if r['result'] == 'TP']
        sl = [r for r in results if r['result'] == 'SL']
        open_trades = [r for r in results if r['result'] == 'Open']

        pnl = sum(r['exit_price'] - r['entry_price']
                  for r in results if r['result'] in ['TP', 'SL'])
        print(f"Wyniki backtestu: TP={len(tp)}, SL={len(sl)}, "
              f"Otwarte={len(open_trades)}, Łączny PnL={pnl:.2f}")


    def plot_backtest(self):
        """
        Wizualizacja wyników backtestu
        :return:
        """
        if self.df is None or not self.backtest_results:
            print("Brak danych do wizualizacji.")
            return

        df = self.df.copy()
        plt.figure(figsize=(14,6))
        plt.plot(df.index, df['close'], label='Close Price')

        for trade in self.backtest_results:
            color = 'green' \
                if trade['result'] == 'TP' \
                else 'red' \
                if trade['result'] == 'SL' \
                else 'gray'
            plt.scatter(trade['entry_time'], trade['entry_price'], color=color, marker='^')
            plt.scatter(trade['exit_time'], trade['exit_price'], color=color, marker='v')

        plt.title(f"Backtest FVG - {self.symbol}")
        plt.xlabel("Czas")
        plt.ylabel("Cena")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    def run(self):
        """
        Uruchomienie strategii
        :return:
        """
        self.get_data()
        self.detect_fvg()
        signals = self.check_price_return()
        return signals


if __name__ == "__main__":
    strategy = FVGStrategy(symbol='ETHUSDT', interval='1m')
    strategy.get_data()
    backtest = strategy.backtest()
    strategy.summarize_backtest()
    strategy.plot_backtest()

    if backtest:
        for backtest_trade in backtest:
            print(backtest_trade)
    else:
        print("Brak sygnałów do backtestu.")
