import enum

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base

# Tworzenie bazy danych SQLite (plik 'database.db')
DATABASE_URL = "sqlite:///database.db"

# Tworzenie silnika bazy danych
engine = create_engine(DATABASE_URL, echo=True)

# Podstawowy model bazy danych
Base = declarative_base()

# Definiowanie Enum w Pythonie
class Side(enum.Enum):
    SELL = "sell"
    BUY = "buy"

# Definicja sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Przykładowy model tabeli
class Trades(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    symbol = Column(String)
    side = Column(Enum(Side), nullable=False)
    price = Column(Float)

# Tworzenie tabel
Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    pass

    # # Tworzenie sesji
    # session = SessionLocal()
    #
    # # Przykładowe dane do dodania
    # new_trade = Trades(
    #     timestamp=datetime.now(),  # Obecny czas
    #     symbol="BTCUSDT",          # Przykładowy symbol
    #     side=Side.BUY,             # Strona transakcji (BUY/SELL)
    #     price=43125.50             # Przykładowa cena
    # )
    # session.add(new_trade)
    # session.commit()
    #
    # # Pobieranie użytkownika
    # trades = session.query(Trades).all()
    # for trade in trades:
    #     print(trade)
    #
    # # Zamknięcie sesji
    # session.close()
