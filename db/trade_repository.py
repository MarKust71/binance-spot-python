from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from db import engine, SessionLocal, Side, Trades


class TradeRepository:
    def __init__(self):
        """Inicjalizacja repozytorium"""
        self.engine = engine
        self.session = SessionLocal()

    def add_trade(self, date_time: datetime,  symbol: str, side: Side, price: float, atr: float):
        """
        Dodaje nową transakcję do bazy danych.
        """
        trade = Trades(
            date_time=date_time,
            symbol=symbol,
            side=side,
            price=price,
            atr=atr,
            stop_loss=round(price - atr if side == Side.BUY else price + atr, 2),
            take_profit=round(price + atr * 2 if side == Side.BUY else price - atr * 2, 2)
        )
        self.session.add(trade)
        try:
            self.session.commit()
        # except Exception as e:
        #     print(e)
        #     self.session.rollback()
        except SQLAlchemyError as e:
            print(f"Błąd podczas aktualizacji transakcji: {e}")
            self.session.rollback()

    def update_trade(self, trade_id: int, **kwargs):
        """
        Aktualizuje istniejącą transakcję o podanym ID w bazie danych.

        :param trade_id: ID transakcji do zaktualizowania
        :param kwargs: Klucz-wartość z polami do aktualizacji (np. price=100.5)
        """
        try:
            trade = self.session.query(Trades).filter_by(id=trade_id).first()
            if trade:
                for key, value in kwargs.items():
                    if hasattr(trade, key):
                        setattr(trade, key, value)
                self.session.commit()
            else:
                print(f"Trade o ID {trade_id} nie istnieje.")
        except SQLAlchemyError as e:
            print(f"Błąd podczas aktualizacji transakcji: {e}")
            self.session.rollback()

    def get_all_trades(self):
        """
        Pobiera wszystkie transakcje z bazy danych.
        """
        return self.session.query(Trades).all()

    def get_trades_by_symbol(self, symbol: str):
        """
        Pobiera wszystkie transakcje dla danego symbolu.
        """
        return self.session.query(Trades).filter(Trades.symbol == symbol).all()

    def get_trade_by_id(self, trade_id: int):
        """
        Pobiera wszystkie transakcje dla danego ID.
        """
        return self.session.query(Trades).filter(Trades.id == trade_id).first()

    def delete_trade(self, trade_id: int):
        """
        Usuwa transakcję na podstawie ID.
        """
        trade = self.session.query(Trades).filter(Trades.id == trade_id).first()
        if trade:
            self.session.delete(trade)
            self.session.commit()

    def close(self):
        """Zamyka sesję"""
        self.session.close()
