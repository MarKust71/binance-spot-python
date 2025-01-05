import pytest, ssl
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock

from helpers import fetch_candles
from api.binance_websocket import ws_connect
from constants import API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL


# Testowanie fetch_candles
@patch("helpers.fetch_candles")
def test_fetch_candles(mock_fetch_candles):
    # Dane testowe
    test_candles = {
        "close": [100, 200, 300]
    }
    mock_fetch_candles.return_value = {"close": test_candles["close"]}

    candles = fetch_candles(TRADE_SYMBOL, KLINE_INTERVAL, 100)
    assert candles["close"][-1] == 300  # Oczekujemy, że ostatni close wynosi 300

# Testowanie websocketu
@patch("api.binance_websocket.ws_connect")
def test_websocket_connection(mock_ws_connect):
    mock_ws = MagicMock()
    mock_ws.run_forever = MagicMock()

    # Zwracamy zamockowany websocket
    mock_ws_connect.return_value = mock_ws

    ws = ws_connect(API_WEBSOCKET_URL, TRADE_SYMBOL, KLINE_INTERVAL)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    # Sprawdzenie, czy run_forever zostało wywołane
    mock_ws.run_forever.assert_called_once_with(sslopt={"cert_reqs": ssl.CERT_NONE})
