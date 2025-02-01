from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Float, Enum, Boolean
from constants import Side

from db.models.models import Base


# Model tabeli trades
class Trades(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, index=True, unique=True)
    symbol = Column(String)
    side = Column(Enum(Side), nullable=False)
    quantity = Column(Float)
    price = Column(Float)
    atr = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return (f"<Trades(id={self.id}, date_time={self.date_time}, symbol={self.symbol}, "
                f"side={self.side}, price={self.price}, atr={self.atr}, "
                f"stop_loss={self.stop_loss}, take_profit={self.take_profit}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})>")

