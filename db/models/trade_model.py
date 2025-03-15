"""
This module defines the Trade model for representing trades in the database.
"""


from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Float, Enum, Boolean
from constants import Side, TradeStatus

from db.models.models import Base


# Model tabeli trades
class Trade(Base):
    """
    Trade model for representing trades in the database.

    :param Base: Base class for creating models.
    :type Base: sqlalchemy.ext.declarative.api.Base

    Attributes:
        id (int): Trade ID.
        date_time (datetime): Trade date and time.
        symbol (str): Trade symbol.
        side (str): Trade side.
        quantity (float): Trade quantity.
        rest_quantity (float): Trade rest quantity.
        price (float): Trade price.
        atr (float): Trade ATR.
        stop_loss (float): Trade stop loss.
        take_profit_partial (float): Trade take profit partial.
        take_profit_safe (float): Trade take profit safe.
        take_profit (float): Trade take profit.
        take_profit_partial_price (float): Trade take profit partial price.
        take_profit_partial_quantity (float): Trade take profit partial quantity.
        take_profit_partial_date_time (datetime): Trade take profit partial date and time.
        take_profit_safe_price (float): Trade take profit safe price.
        take_profit_safe_quantity (float): Trade take profit safe quantity.
        take_profit_safe_date_time (datetime): Trade take profit safe date and time.
        close_price (float): Trade close price.
        close_date_time (datetime): Trade close date and time.
        profit (float): Trade profit.
        is_closed (bool): Trade is closed.
        status (str): Trade status.
        created_at (datetime): Trade created at.
        updated_at (datetime): Trade updated at.
    """
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, index=True, unique=True)
    symbol = Column(String)
    side = Column(Enum(Side), nullable=False)
    quantity = Column(Float)
    rest_quantity = Column(Float)
    price = Column(Float)
    atr = Column(Float)
    stop_loss = Column(Float)
    take_profit_partial = Column(Float)
    take_profit_safe = Column(Float)
    take_profit = Column(Float)
    take_profit_partial_price = Column(Float)
    take_profit_partial_quantity = Column(Float)
    take_profit_partial_date_time = Column(DateTime)
    take_profit_safe_price = Column(Float)
    take_profit_safe_quantity = Column(Float)
    take_profit_safe_date_time = Column(DateTime)
    close_price = Column(Float)
    close_date_time = Column(DateTime)
    profit = Column(Float)
    is_closed = Column(Boolean, default=False)
    status = Column(Enum(TradeStatus), nullable=False, default=TradeStatus.NONE)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


    def __repr__(self):
        return (f"<Trades(id={self.id}, date_time={self.date_time}, symbol={self.symbol}, "
                f"side={self.side}, quantity={self.quantity}, rest_quantity={self.rest_quantity}, "
                f"price={self.price}, atr={self.atr}, stop_loss={self.stop_loss}, "
                f"take_profit={self.take_profit}, close_price={self.close_price}, "
                f"take_profit_partial={self.take_profit_partial}, "
                f"take_profit_safe={self.take_profit_safe}, "
                f"take_profit_partial_price={self.take_profit_partial_price}, "
                f"take_profit_partial_quantity={self.take_profit_partial_quantity}, "
                f"take_profit_partial_date_time={self.take_profit_partial_date_time}, "
                f"take_profit_safe_price={self.take_profit_safe_price}, "
                f"take_profit_safe_quantity={self.take_profit_safe_quantity}, "
                f"take_profit_safe_date_time={self.take_profit_safe_date_time}, "
                f"is_closed={self.is_closed}, status={self.status}, "
                f"close_date_time={self.close_date_time}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})>")


    def as_dict(self):
        """
        Converts the Trade object to a dictionary.

        :return: A dictionary representation of the Trade object
        """
        return {
            'id': self.id,
            'date_time': self.date_time,
            'symbol': self.symbol,
            'side': self.side,
            'quantity': self.quantity,
            'rest_quantity': self.rest_quantity,
            'price': self.price,
            'atr': self.atr,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'take_profit_partial': self.take_profit_partial,
            'take_profit_safe': self.take_profit_safe,
            'close_price': self.close_price,
            'take_profit_partial_price': self.take_profit_partial_price,
            'take_profit_partial_quantity': self.take_profit_partial_quantity,
            'take_profit_partial_date_time': self.take_profit_partial_date_time,
            'take_profit_safe_price': self.take_profit_safe_price,
            'take_profit_safe_quantity': self.take_profit_safe_quantity,
            'take_profit_safe_date_time': self.take_profit_safe_date_time,
            'is_closed': self.is_closed,
            'status': self.status,
            'close_date_time': self.close_date_time,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
