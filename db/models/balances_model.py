"""
This module defines the Balance model for representing the balance of an asset.
"""


from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float, String

from db.models.models import Base


# Model tabeli balances
class Balance(Base):
    """
    Model representing the balance of an asset.
    """
    # pylint: disable=too-few-public-methods
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    asset = Column(String, index=True, unique=True)
    free = Column(Float)
    locked = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return (f"<Balances(id={self.id}, asset={self.asset}, free={self.free}, "
                f"locked={self.locked}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})>")
