def db_delete_all_trades():
    from db.repositories import TradeRepository

    trades_repo = TradeRepository()
    trades_repo.delete_all_trades()


if __name__ == '__main__':
    db_delete_all_trades()
