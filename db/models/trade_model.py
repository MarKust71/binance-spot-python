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
    Represents a trade in the database.

    Attributes:
        id (int): The unique identifier of the trade.
        date_time (datetime): The date and time of the trade.
        symbol (str): The symbol of the traded asset.
        side (Side): The side of the trade (buy/sell).
        quantity (float): The quantity of the traded asset.
        rest_quantity (float): The remaining quantity of the traded asset.
        price (float): The price at which the trade was executed.
        atr (float): The average true range of the asset.
        stop_loss (float): The stop loss price.
        take_profit_partial (float): The partial take profit price.
        take_profit_partial_price (float): The price for partial take profit.
        take_profit_partial_quantity (float): The quantity for partial take profit.
        take_profit_partial_date_time (datetime): The date and time for partial take profit.
        take_profit (float): The take profit price.
        close_price (float): The closing price of the trade.
        profit (float): The profit of the trade.
        is_closed (bool): Indicates if the trade is closed.
        status (TradeStatus): Trade status
        close_date_time (datetime): The date and time when the trade was closed.
        created_at (datetime): The date and time when the trade was created.
        updated_at (datetime): The date and time when the trade was last updated.
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
    take_profit_partial_price = Column(Float)
    take_profit_partial_quantity = Column(Float)
    take_profit_partial_date_time = Column(DateTime)
    take_profit = Column(Float)
    close_price = Column(Float)
    profit = Column(Float)
    is_closed = Column(Boolean, default=False)
    status = Column(Enum(TradeStatus), nullable=False)
    close_date_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


    def __repr__(self):
        return (f"<Trades(id={self.id}, date_time={self.date_time}, symbol={self.symbol}, "
                f"side={self.side}, quantity={self.quantity}, rest_quantity={self.rest_quantity}, "
                f"price={self.price}, atr={self.atr}, stop_loss={self.stop_loss}, "
                f"take_profit={self.take_profit}, close_price={self.close_price}, "
                f"take_profit_partial={self.take_profit_partial}, "
                f"take_profit_partial_price={self.take_profit_partial_price}, "
                f"take_profit_partial_quantity={self.take_profit_partial_quantity}, "
                f"take_profit_partial_date_time={self.take_profit_partial_date_time}, "
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
            'close_price': self.close_price,
            'take_profit_partial': self.take_profit_partial,
            'take_profit_partial_price': self.take_profit_partial_price,
            'take_profit_partial_quantity': self.take_profit_partial_quantity,
            'take_profit_partial_date_time': self.take_profit_partial_date_time,
            'is_closed': self.is_closed,
            'status': self.status,
            'close_date_time': self.close_date_time,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
