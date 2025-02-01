from datetime import datetime

from db.database import engine, SessionLocal
from db.models import Balances


class BalancesRepository:
    def __init__(self):
        self.engine = engine
        self.session = SessionLocal()


    def add_asset(self, asset):
        balance = Balances(
            asset=asset,
            free=0,
            locked=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.session.add(balance)
        self.session.commit()


    def get_balance_by_asset(self, asset):
        balance = self.session.query(Balances).filter_by(asset=asset).first()
        return balance


    def set_balance(self, asset, **kwargs):
        balance = self.session.query(Balances).filter_by(asset=asset).first()
        if balance:
            for key, value in kwargs.items():
                if hasattr(balance, key):
                    setattr(balance, key, value)
            balance.updated_at = datetime.now()
            self.session.commit()
        pass


    def get_all_balances(self):
        balances = self.session.query(Balances).all()
        return balances


    def delete_balance(self, asset):
        balance = self.session.query(Balances).filter_by(asset=asset).first()
        self.session.delete(balance)
        self.session.commit()


    def close(self):
        """Zamyka sesję"""
        self.session.close()


if __name__ == '__main__':
    pass

    repo = BalancesRepository()

    # Dodanie przykładowego salda
    repo.add_asset(asset="USDT")
    repo.add_asset(asset="ETH")

    # # Pobranie i wyświetlenie salda
    # balances = repo.get_all_balances()
    # print(balances)

    # Aktualizacja salda
    repo.set_balance(asset="USDT", free=100)
    repo.set_balance(asset="ETH", free=0.1)

    # # Pobranie i wyświetlenie salda
    # balances = repo.get_all_balances()
    # print(balances)

    # # Usunięcie salda
    # repo.delete_balance(asset="USDT")

    # # Pobranie i wyświetlenie salda
    # balances = repo.get_all_balances()
    # print(balances)

    repo.close()
