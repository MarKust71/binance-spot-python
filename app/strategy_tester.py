# strategy_tester.py
"""
Strategy tester module.
"""
from constants import TRADE_SYMBOL, KLINE_INTERVAL, KLINE_TREND_INTERVAL
from db.utils import db_update_trades, db_add_trade
from db.repositories import TradeRepository
from helpers import fetch_candles

LIMIT = 1000
SCOPE = 2
TREND_LIMIT = 1000
FRACTALS_PERIODS = 8
DELAY = 0


def strategy_tester():
    """
    Strategy tester function.
    """
    candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_INTERVAL, limit=LIMIT, end_time=None
    )
    trend_candles = fetch_candles(
        symbol=TRADE_SYMBOL, interval=KLINE_TREND_INTERVAL, limit=TREND_LIMIT, end_time=None
    )

    # tc = set_fractals(trend_candles, periods=FRACTALS_PERIODS)
    # fr = tc[tc['Fractal_Up'].notnull() | tc['Fractal_Down'].notnull()][['timestamp',
    # 'Fractal_Down', 'Fractal_Up']]
    # print(fr)
    # fr.to_csv('fractals.csv')

    # candles.to_csv('candles.csv')
    # trend_candles.to_csv('trend_candles.csv')

    for i in range(0, len(candles) - SCOPE + 1):

        data = candles.iloc[:SCOPE + i]

        new_trade_id = db_add_trade(
            candles=data,
            trend_candles=trend_candles,
            delay=DELAY,
            fractals_periods=FRACTALS_PERIODS,
        )

        if new_trade_id != -1 and new_trade_id is not None:
            print(f'New trade created, ID: {new_trade_id}\n')

        db_update_trades(
            symbol=TRADE_SYMBOL,
            price=data["close"].to_numpy()[-1],
            timestamp=data['timestamp'].iloc[-1],
        )




if __name__ == '__main__':
    strategy_tester()

    trades_repo = TradeRepository()
    trades_repo.report_results()
    trades_repo.close()




    # trades_repo = TradeRepository()
    #
    # # Dodanie przykładowej transakcji
    # trades_repo.add_trade(symbol="ETHUSDT", side=Side.BUY, price=3125.50, atr=8.8)
    #
    # # Pobranie i wyświetlenie transakcji
    # trades = trades_repo.get_all_trades()
    # for trade in trades:
    #     print(trade)
    #
    # trade = trades_repo.get_trade_by_id(33)
    # print(trade)
    # print(trade.stop_loss)
    #
    # trades_repo.close()
