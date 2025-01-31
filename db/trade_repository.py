from datetime import datetime
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
        except Exception as e:
            print(e)
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
