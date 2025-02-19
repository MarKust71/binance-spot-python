"""
This module provides the BalancesRepository class for managing balances in the database.
"""


from datetime import datetime

from db.database import engine, SessionLocal
from db.models import Balance


class BalancesRepository:
    """
    Repository class for managing balances in the database.
    Provides methods to add, retrieve, update, and delete balances.
    """
    def __init__(self):
        self.engine = engine
        self.session = SessionLocal()


    def add_asset(self, asset):
        """
        Adds a new asset with initial balance to the database.

        :param asset: The asset to be added
        """
        balance = Balance(
            asset=asset,
            free=0,
            locked=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.session.add(balance)
        self.session.commit()


    def get_balance_by_asset(self, asset):
        """
        Retrieves the balance for a given asset from the database.

        :param asset: The asset whose balance is to be retrieved
        :return: The balance of the specified asset
        """
        balance = self.session.query(Balance).filter_by(asset=asset).first()
        return balance


    def set_balance(self, asset, **kwargs):
        """
        Updates the balance for a given asset with the provided key-value pairs.

        :param asset: The asset to update the balance for
        :param kwargs: Key-value pairs of balance attributes to update (e.g., free=100)
        """
        balance = self.session.query(Balance).filter_by(asset=asset).first()
        if balance:
            for key, value in kwargs.items():
                if hasattr(balance, key):
                    setattr(balance, key, value)
            balance.updated_at = datetime.now()
            self.session.commit()


    def get_all_balances(self):
        """
        Retrieves all balances from the database.

        :return: A list of all balances
        """
        balances = self.session.query(Balance).all()
        return balances


    def delete_balance(self, asset):
        """
        Deletes the balance for a given asset from the database.

        :param asset: The asset whose balance is to be deleted
        """
        balance = self.session.query(Balance).filter_by(asset=asset).first()
        self.session.delete(balance)
        self.session.commit()


    def close(self):
        """Zamyka sesję"""
        self.session.close()


if __name__ == '__main__':
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
