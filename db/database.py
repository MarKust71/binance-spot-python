import enum

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base

# # Tworzenie bazy danych SQLite (plik 'database.db')
# DATABASE_URL = "sqlite:///database.db"

from pathlib import Path

# Pobranie ścieżki do katalogu głównego aplikacji
BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

# # Tworzenie katalogu 'db' jeśli nie istnieje
# DB_DIR = BASE_DIR / 'db'
# DB_DIR.mkdir(exist_ok=True)

# Ustawienie ścieżki do pliku bazy danych
# DATABASE_URL = f"sqlite:///{DB_DIR / 'database.db'}"
DATABASE_URL = f"sqlite:///{BASE_DIR / 'database.db'}"

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
    date_time = Column(DateTime, index=True)
    symbol = Column(String)
    side = Column(Enum(Side), nullable=False)
    price = Column(Float)
    atr = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    timestamp = Column(DateTime, default=datetime.now, index=True)

# Tworzenie tabel
Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    pass

    # Przykładowe dane do dodania
    new_trade = Trades(
        date_time=datetime.now(),
        symbol="ETHUSDT",          # Przykładowy symbol
        side=Side.BUY,             # Strona transakcji (BUY/SELL)
        price=3125.50,             # Przykładowa cena
        atr=8.8,
        stop_loss=3125.50 - 8.8,
        take_profit=3125.50 + 8.8 * 2,
        timestamp=datetime.now()  # Obecny czas
    )

    if new_trade.price > 0:
        # Tworzenie sesji
        session = SessionLocal()

        session.add(new_trade)
        session.commit()

        # Pobieranie użytkownika
        trades = session.query(Trades).all()
        for trade in trades:
            print(trade)

        # Zamknięcie sesji
        session.close()
