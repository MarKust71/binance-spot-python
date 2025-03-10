"""
This module initializes the FastAPI application and defines the API endpoints
for interacting with the trades database. It includes functionality for
pagination and sorting of trade data.
"""
import asyncio

from fastapi import FastAPI, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from db.database import DATABASE_URL
from db.models import Trade

# Konfiguracja bazy danych
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Inicjalizacja FastAPI
app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Funkcja zależności do pobierania sesji
def get_db():
    """
    Dependency function that provides a database session.
    Yields:
        db (Session): SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Lista połączeń WebSocket
active_connections = set()

# Endpoint dla WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that accepts incoming connections and broadcasts messages
    :param websocket:
    :return:
    """
    await websocket.accept()
    print(websocket)
    active_connections.add(websocket)
    print(f"Active connections: {active_connections}")
    try:
        while True:
            message = await websocket.receive_text()  # Oczekujemy na dane, ale nie przetwarzamy ich
            print(f"Received message: {message}")
            if message == "ping":
                await send_websocket_message("pong")
            else:
                await send_websocket_message(message)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def send_websocket_message(message: str):
    """
    Sends a message to all active WebSocket connections
    :param message:
    :return:
    """
    if active_connections:
        print(f"Sending websocket message: {message}")
        await asyncio.gather(*(ws.send_text(message) for ws in active_connections))
    else:
        print("No active connections")


# Endpoint zwracający dane z tabeli z mechanizmem stronicowania
@app.get("/api/trades/", response_model=dict)
def read_items(
        db: Session = Depends(get_db),
        skip: int = Query(0, alias="offset", ge=0),
        limit: int = Query(10, alias="limit", ge=1)
):
    """
    Retrieves trade data from the database with pagination and sorting.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of records to skip for pagination.
        limit (int): Maximum number of records to return.

    Returns:
        dict: A dictionary containing trade data and pagination information.
    """
    # Sortowanie po date_time malejąco
    trades_query = db.query(Trade).order_by(Trade.date_time.desc())

    # Pobranie danych z uwzględnieniem offset i limit
    trades = trades_query.offset(skip).limit(limit).all()

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
            "status": trade.status,
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


if __name__ == '__main__':
    # Uruchomienie serwera komendą:
    # uvicorn script_name:app --reload --host 0.0.0.0 --port 8000
    #
    # http://127.0.0.1:8000/items/?offset=0&limit=5

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
