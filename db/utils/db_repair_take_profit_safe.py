"""
Repairs take_profit_safe values.
"""
from db.repositories import TradeRepository


def db_repair_take_profit_safe():
    """
    Deletes all trades from the database.
    """
    trades_repo = TradeRepository()
    trades_repo.repair_take_profit_safe()


if __name__ == '__main__':
    db_repair_take_profit_safe()
    print("All trades (take_profit_safe) repaired.")
