import pandas as pd
from pandas import DataFrame

from db.repositories import TradeRepository


def db_list_trades() -> DataFrame:
    trades_repo = TradeRepository()
    trades = trades_repo.get_all_trades()

    return pd.DataFrame([trade.as_dict() for trade in trades])


if __name__ == '__main__':
    df = db_list_trades()

    print(df)
