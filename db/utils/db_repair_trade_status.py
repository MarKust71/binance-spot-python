"""
Repairs trade_status values.
"""
from db.repositories import TradeRepository


def db_repair_trade_status():
    """
    Deletes all trades from the database.
    """
    trades_repo = TradeRepository()
    trades_repo.repair_trade_status()


if __name__ == '__main__':
    db_repair_trade_status()
    print("All trades (trade_status) repaired.")
