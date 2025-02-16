"""
This module contains the TradeRepository class for managing trade operations in the database.
"""


from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError

from constants import Side, TradeStatus
from db.database import engine, SessionLocal
from db.models.trade_model import Trade

TP_SL_FACTOR = 3
TP_SL = 5


@dataclass
class TradeData:
    """
    A data class representing the details of a trade.
    """
    date_time: datetime
    symbol: str
    side: Side
    price: float
    quantity: float
    atr: float


class TradeRepository:
    """
    A repository class for managing trade operations in the database.
    """
    def __init__(self):
        """Inicjalizacja repozytorium"""
        self.engine = engine
        self.session = SessionLocal()


    def add_trade(self, trade_data: TradeData) -> int | None:
        """
        Dodaje nową transakcję do bazy danych.
        """
        trade_args = {
            'date_time': trade_data.date_time,
            'symbol': trade_data.symbol,
            'side': trade_data.side,
            'price': trade_data.price,
            'quantity': trade_data.quantity,
            'rest_quantity': trade_data.quantity,
            'atr': trade_data.atr,
            'stop_loss': round(
                trade_data.price - TP_SL
                if trade_data.side == Side.BUY
                else trade_data.price + TP_SL,
                2
            ),
            'take_profit_partial': round(
                trade_data.price + TP_SL
                if trade_data.side == Side.BUY
                else trade_data.price - TP_SL,
                2
            ),
            'take_profit': round(
                trade_data.price + TP_SL * TP_SL_FACTOR
                if trade_data.side == Side.BUY
                else trade_data.price - TP_SL * TP_SL_FACTOR,
                2
            ),
            'status': TradeStatus.OPEN,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        trade = Trade(**trade_args)
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


    def repair_trade_status(self):
        """
        Aktualizuje status transakcji w bazie danych na podstawie warunków:
        - 'CLOSED', jeśli is_closed == 1
        - 'PARTIAL', jeśli is_closed == 0 i take_profit_datetime nie jest puste
        - 'OPEN' w pozostałych przypadkach
        """
        try:
            self.session.query(Trade).update(
                {
                    Trade.status: case(
                (Trade.is_closed == 1, TradeStatus.CLOSED),
                        ((Trade.is_closed == 0)
                         & (
                             Trade.take_profit_partial_date_time.isnot(None)
                         ), TradeStatus.PARTIAL),
                        else_=TradeStatus.OPEN
                    )
                },
                synchronize_session=False
            )
            self.session.commit()
        except SQLAlchemyError as e:
            print(f"Błąd podczas aktualizacji statusów transakcji: {e}")
            self.session.rollback()


    def close(self):
        """Zamyka sesję"""
        self.session.close()
