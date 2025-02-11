from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from constants import Side
from db.database import engine, SessionLocal
from db.models.trade_model import Trade

TP_SL_FACTOR = 3
TP_SL = 5

class TradeRepository:
    def __init__(self):
        """Inicjalizacja repozytorium"""
        self.engine = engine
        self.session = SessionLocal()


    def add_trade(
            self,
            date_time: datetime,
            symbol: str,
            side: Side,
            price: float,
            quantity: float,
            atr: float
    ) -> int | None:
        """
        Dodaje nową transakcję do bazy danych.
        """
        trade = Trade(
            date_time=date_time,
            symbol=symbol,
            side=side,
            price=price,
            quantity=quantity,
            rest_quantity=quantity,
            atr=atr,
            # stop_loss=round(price - atr if side == Side.BUY else price + atr, 2),
            # take_profit_partial=round(price + atr if side == Side.BUY else price - atr, 2),
            # take_profit=round(price + atr * TP_SL_FACTOR if side == Side.BUY else price - atr * TP_SL_FACTOR, 2),
            stop_loss=round(price - TP_SL if side == Side.BUY else price + TP_SL, 2),
            take_profit_partial=round(price + TP_SL if side == Side.BUY else price - TP_SL, 2),
            take_profit=round(price + TP_SL * TP_SL_FACTOR if side == Side.BUY else price - TP_SL * TP_SL_FACTOR, 2),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.session.add(trade)

        try:
            self.session.commit()
            return trade.id

        except SQLAlchemyError as e:
            print(f"Błąd podczas aktualizacji transakcji: {e}")
            self.session.rollback()
            return None


    def update_trade(self, trade_id: int, **kwargs):
        """
        Aktualizuje istniejącą transakcję o podanym ID w bazie danych.

        :param trade_id: ID transakcji do zaktualizowania
        :param kwargs: Klucz-wartość z polami do aktualizacji (np. price=100.5)
        """
        try:
            trade = self.session.query(Trade).filter_by(id=trade_id).first()
            if trade:
                for key, value in kwargs.items():
                    if hasattr(trade, key):
                        setattr(trade, key, value)

                trade.updated_at = datetime.now()

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
        return self.session.query(Trade).all()


    def get_trades_by_symbol(self, symbol: str):
        """
        Pobiera wszystkie transakcje dla danego symbolu.
        """
        return self.session.query(Trade).filter(Trade.symbol == symbol).all()


    def get_trade_by_id(self, trade_id: int):
        """
        Pobiera wszystkie transakcje dla danego ID.
        """
        return self.session.query(Trade).filter(Trade.id == trade_id).first()


    def delete_trade(self, trade_id: int):
        """
        Usuwa transakcję na podstawie ID.
        """
        trade = self.session.query(Trade).filter(Trade.id == trade_id).first()
        if trade:
            self.session.delete(trade)
            self.session.commit()


    def delete_all_trades(self):
        """
        Usuwa wszystkie transakcje.
        """
        self.session.query(Trade).delete()
        self.session.commit()


    def close(self):
        """Zamyka sesję"""
        self.session.close()
