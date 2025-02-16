"""
This module deletes all trades from the database.
"""

from db.repositories import TradeRepository

def db_delete_all_trades():
    """
    Deletes all trades from the database.
    """
    trades_repo = TradeRepository()
    trades_repo.delete_all_trades()


if __name__ == '__main__':
    db_delete_all_trades()
