from fastapi import FastAPI, Depends, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from typing import List

from db.database import DATABASE_URL
from db.models import Trade

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Inicjalizacja FastAPI
app = FastAPI()

# Funkcja zależności do pobierania sesji
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint zwracający dane z tabeli z mechanizmem stronicowania
@app.get("/api/trades/", response_model=dict)
def read_items(
        db: Session = Depends(get_db),
        skip: int = Query(0, alias="offset", ge=0),
        limit: int = Query(10, alias="limit", ge=1)
):
    trades = db.query(Trade).offset(skip).limit(limit).all()
    total = db.query(Trade).count()
    return {
        "data": [{
            "id": trade.id,
            "date_time": trade.date_time,
            "symbol": trade.symbol,
            "side": trade.side,
            "quantity": trade.quantity,
            "rest_quantity": trade.rest_quantity,
            "price": trade.price,
            "atr": trade.atr,
            "stop_loss": trade.stop_loss,
            "take_profit_partial": trade.take_profit_partial,
            "take_profit_partial_price": trade.take_profit_partial_price,
            "take_profit_partial_quantity": trade.take_profit_partial_quantity,
            "take_profit_partial_date_time": trade.take_profit_partial_date_time,
            "take_profit": trade.take_profit,
            "close_price": trade.close_price,
            "profit": trade.profit,
            "is_closed": trade.is_closed,
            "close_date_time": trade.close_date_time,
            "created_at": trade.created_at,
            "updated_at": trade.updated_at}
            for trade in trades],
        "pagination": {
            "total": total,
            "offset": skip,
            "limit": limit,
            "has_next": skip + limit < total
        }
    }

# Uruchomienie serwera komendą:
# uvicorn script_name:app --reload --host 0.0.0.0 --port 8000
#
# http://127.0.0.1:8000/items/?offset=0&limit=5


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
