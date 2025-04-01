"""
Database configuration and setup module.
"""


from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models.models import Base

# Pobranie ścieżki do katalogu głównego aplikacji
BASE_DIR = Path(__file__).resolve().parent

# Ustawienie ścieżki do pliku bazy danych
DATABASE_URL = f"sqlite:///{BASE_DIR / 'database.sqlite'}"

# Tworzenie silnika bazy danych
engine = create_engine(DATABASE_URL, echo=False)

# Definicja sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tworzenie tabel
Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    pass

    # # Przykładowe dane do dodania
    # new_trade = Trades(
    #     date_time=datetime.now(),
    #     symbol="ETHUSDC",          # Przykładowy symbol
    #     side=Side.BUY,             # Strona transakcji (BUY/SELL)
    #     price=3125.50,             # Przykładowa cena
    #     quantity=round(60 / 3125.50, 4),     # Przykładowa ilość
    #     atr=8.8,
    #     stop_loss=3125.50 - 8.8,
    #     take_profit=3125.50 + 8.8 * 2,
    # )
    #
    # if new_trade.price > 0:
    #     # Tworzenie sesji
    #     session = SessionLocal()
    #
    #     session.add(new_trade)
    #     session.commit()
    #
    #     # Pobieranie użytkownika
    #     trades = session.query(Trades).all()
    #     for trade in trades:
    #         print(trade)
    #
    #     # Zamknięcie sesji
    #     session.close()
