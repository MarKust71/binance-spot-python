"""
This module retrieves all trades from the database and returns them as a DataFrame.
"""


import pandas as pd
from pandas import DataFrame

from db.repositories import TradeRepository


def db_list_trades() -> DataFrame:
    """
    Retrieves all trades from the database and returns them as a DataFrame.

    Returns:
        DataFrame: A DataFrame containing all trades.
    """
    trades_repo = TradeRepository()
    trades = trades_repo.get_all_trades()

    return pd.DataFrame([trade.as_dict() for trade in trades])


if __name__ == '__main__':
    df = db_list_trades()

    print(df)
