"""
This module initializes the FastAPI application and defines the API endpoints
for interacting with the trades database. It includes functionality for
pagination and sorting of trade data.
"""
import asyncio

from typing import List, Optional
from fastapi import FastAPI, Depends, Query, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from constants import TradeStatus
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
                await send_message("pong")
            else:
                await send_message(message)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def send_message(message: str):
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
def parse_exclude_status(
        raw_statuses: Optional[List[str]] = Query(default=None, alias="exclude_status")
) -> Optional[List[TradeStatus]]:
    """
    Parsuje wartości statusów zapytania i zwraca listę obiektów TradeStatus.
    :param raw_statuses:
    :return:
    """
    if not raw_statuses:
        return None

    result = []
    for value in raw_statuses:
        if not value.strip():  # pomiń puste ciągi
            continue
        try:
            result.append(TradeStatus(value.strip()))
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status value: {value}"
            ) from exc
    return result if result else None

@app.get("/api/trades/", response_model=dict)
def read_items(
        db: Session = Depends(get_db),
        skip: int = Query(0, alias="offset", ge=0),
        limit: int = Query(10, alias="limit", ge=1),
        exclude_status: Optional[List[TradeStatus]] = Depends(parse_exclude_status)
):
    """
    Retrieves trade data from the database with pagination and sorting.
    Allows excluding specific trade statuses via multiple query parameters.

    Args:
        db (Session): SQLAlchemy database session.
        skip (int): Number of records to skip for pagination.
        limit (int): Maximum number of records to return.
        exclude_status (Optional[List[TradeStatus]]): List of trade statuses to exclude.

    Returns:
        dict: A dictionary containing trade data and pagination information.
    """
    # ✅ Walidacja niepotrzebna – FastAPI i Enum automatycznie zgłaszają błąd 422,
    #    jeśli ktoś poda np. `exclude_statuses=invalid`
    # ✅ Można jednak dorzucić własny komunikat (opcjonalnie):

    print(f'exclude_status: {exclude_status}')

    invalid_statuses = []
    if exclude_status:
        for status in exclude_status:
            if status not in TradeStatus:
                invalid_statuses.append(status)

    if invalid_statuses:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid status values: {invalid_statuses}"
        )

    # Sortowanie po date_time malejąco
    trades_query = db.query(Trade).order_by(Trade.date_time.desc())

    # Filtrowanie po statusach
    if exclude_status:
        trades_query = trades_query.filter(~Trade.status.in_(exclude_status))

    # Pobranie danych z uwzględnieniem offset i limit
    trades = trades_query.offset(skip).limit(limit).all()

    # total = db.query(Trade).count()
    # total = db.query(Trade).filter(~Trade.status.in_(exclude_status)).count() if exclude_status else db.query(Trade).count()
    total = trades_query.count()

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
            "take_profit_safe": trade.take_profit_safe,
            "take_profit": trade.take_profit,
            "take_profit_partial_price": trade.take_profit_partial_price,
            "take_profit_partial_quantity": trade.take_profit_partial_quantity,
            "take_profit_partial_date_time": trade.take_profit_partial_date_time,
            "take_profit_safe_price": trade.take_profit_safe_price,
            "take_profit_safe_quantity": trade.take_profit_safe_quantity,
            "take_profit_safe_date_time": trade.take_profit_safe_date_time,
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
