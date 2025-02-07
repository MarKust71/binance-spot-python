from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Float, Enum, Boolean
from constants import Side

from db.models.models import Base


# Model tabeli trades
class Trade(Base):
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
    close_date_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return (f"<Trades(id={self.id}, date_time={self.date_time}, symbol={self.symbol}, "
                f"side={self.side}, quantity={self.quantity}, rest_quantity={self.rest_quantity}, price={self.price}, "
                f"atr={self.atr}, stop_loss={self.stop_loss}, take_profit={self.take_profit}, "
                f"close_price={self.close_price}, take_profit_partial={self.take_profit_partial}, "
                f"take_profit_partial_price={self.take_profit_partial_price}, "
                f"take_profit_partial_quantity={self.take_profit_partial_quantity}, "
                f"take_profit_partial_date_time={self.take_profit_partial_date_time}, is_closed={self.is_closed}, "
                f"close_date_time={self.close_date_time}, created_at={self.created_at}, updated_at={self.updated_at})>")

    def as_dict(self):
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
            'close_date_time': self.close_date_time,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
