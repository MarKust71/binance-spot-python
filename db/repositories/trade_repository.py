"""
This module contains the TradeRepository class for managing trade operations in the database.
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

import pandas as pd

from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError

from constants import (Side, TradeStatus, APPLY_TAKE_PROFIT, APPLY_TAKE_PROFIT_SAFE,
                       TP_SL, TP_SL_FACTOR)
from db.database import engine, SessionLocal
from db.models.trade_model import Trade
from db.utils.to_decimal import to_decimal


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
        self.trades: List[Trade] = []


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
            'take_profit_safe': round(
                trade_data.price + TP_SL * 2
                if trade_data.side == Side.BUY
                else trade_data.price - TP_SL * 2,
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
        self.trades = self.session.query(Trade).all()

        # return self.session.query(Trade).all()
        return self.trades

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


    def get_trades_by_symbol_older_than_timestamp(
            self,
            is_closed: bool,
            symbol: str,
            time_from: pd.Timestamp
    ):
        """
        Zwraca wszystkie rekordy spełniające warunki:
        - symbol zgodny z parametrem 'symbol',
        - data i czas rekordu większy lub równy parametrowi 'timestamp',
        - wartość is_closed różna od parametru 'is_closed'.

        :param is_closed: bool - oczekiwana wartość pola is_closed (najczęściej False)
        :param symbol: str - symbol, dla którego filtrowane są rekordy
        :param time_from: datetime - data i czas, od którego filtrowane są rekordy
        :return: lista rekordów spełniających powyższe warunki
        """
        return self.session.query(Trade).filter(
            Trade.symbol == symbol,
            Trade.date_time < time_from,
            Trade.is_closed == is_closed
        ).all()


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


    def repair_take_profit_safe(self):
        """
        Naprawia wartość pola take_profit_safe
        """
        try:
            self.session.query(Trade).update(
                {
                    Trade.take_profit_safe: case(
                        (Trade.side == Side.BUY, Trade.price + TP_SL * 2),
                        (Trade.side == Side.SELL, Trade.price - TP_SL * 2),
                        else_=Trade.take_profit_safe
                    )
                },
                synchronize_session=False
            )
            self.session.commit()
        except SQLAlchemyError as e:
            print(f"Błąd podczas naprawy pola take_profit_safe: {e}")
            self.session.rollback()


    def repair_trade_status(self):
        """
        Aktualizuje status transakcji w bazie danych na podstawie warunków:
        - 'CLOSED', jeśli is_closed == 1
        - 'SAFE', jeśli is_closed == 0
            i take_profit_safe_date_time NIE JEST puste
            i take_profit_partial_date_time NIE JEST puste
        - 'PARTIAL', jeśli is_closed == 0
            i take_profit_partial_date_time NIE JEST puste
            i take_profit_safe_date_time JEST puste
        - 'OPEN' w pozostałych przypadkach
        """
        try:
            self.session.query(Trade).update(
                {
                    Trade.status: case(
                (Trade.is_closed == 1, TradeStatus.CLOSED),
                        (
                            (Trade.is_closed == 0)
                            & (Trade.take_profit_partial_date_time.isnot(None))
                            & (Trade.take_profit_safe_date_time.isnot(None)),
                            TradeStatus.SAFE
                        ),
                        (
                            (Trade.is_closed == 0)
                            & (Trade.take_profit_partial_date_time.isnot(None))
                            & (Trade.take_profit_safe_date_time.is_(None)),
                            TradeStatus.PARTIAL
                        ),
                        else_=TradeStatus.OPEN
                    )
                },
                synchronize_session=False
            )
            self.session.commit()
        except SQLAlchemyError as e:
            print(f"Błąd podczas aktualizacji statusów transakcji: {e}")
            self.session.rollback()


    def get_total_profit_by_status(self, status: Optional[TradeStatus] = None) -> Decimal('0.00'):
        """
        Zwraca sumę zysku transakcji spełniających warunki:
        :param status:
        :return:
        """
        return sum(
            (to_decimal(trade.profit) for trade in self.trades
             if status is None or trade.status == status),
            Decimal('0.00')
        )


    def count_by_status_and_profit_sign(
            self,
            positive: bool = True,
            status: Optional[TradeStatus] = None
    ) -> int:
        """
        Zwraca liczbę transakcji spełniających warunki:
        :param positive:
        :param status:
        :return:
        """
        if positive:
            return sum(
                1 for trade in self.trades
                if (status is None or trade.status == status) and trade.profit >= 0
            )

        return sum(
            1 for trade in self.trades
            if (status is None or trade.status == status) and trade.profit < 0
        )


    def report_results(self):
        """
        Raportuje wyniki transakcji.
        """
        self.get_all_trades()
        total_profit = self.get_total_profit_by_status(status=TradeStatus.CLOSED)
        partial_profit = self.get_total_profit_by_status(status=TradeStatus.PARTIAL)
        open_profit = self.get_total_profit_by_status(status=TradeStatus.OPEN)
        profits = self.count_by_status_and_profit_sign(positive=True, status=TradeStatus.CLOSED)
        loses = self.count_by_status_and_profit_sign(positive=False, status=TradeStatus.CLOSED)

        print(f'Apply T/P: {APPLY_TAKE_PROFIT}, Apply T/P Safe: {APPLY_TAKE_PROFIT_SAFE}, '
              f'TP/SL: {to_decimal(TP_SL_FACTOR)}')
        print(f'Total profit: {total_profit}, profits: {profits}, loses: {loses}')
        print(f'Partial profit: {partial_profit}, open profit: {open_profit}')


    def close(self):
        """Zamyka sesję"""
        self.session.close()


if __name__ == '__main__':
    trades_repo = TradeRepository()
    trades_repo.report_results()
    trades_repo.close()
