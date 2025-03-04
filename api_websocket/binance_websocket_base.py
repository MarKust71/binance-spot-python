"""
Binance WebSocket base class to manage WebSocket connection with auto-reconnect.
"""
import ssl
import time
from datetime import datetime
from websocket import WebSocketApp


class BinanceWebSocketBase:
    """Base class to manage Binance WebSocket connection with auto-reconnect."""

    def __init__(self, url: str, symbol: str):
        self.url = url
        self.symbol = symbol
        self.ws = None
        self.last_open_time = None

    def on_error(self, _ws, error) -> None:
        """Handles WebSocket errors."""
        print(f'\033[91m{self.get_log_prefix()}\033[0m-> error {error}')

    def on_open(self, _ws) -> None:
        """Handles WebSocket opening."""
        self.last_open_time = time.time()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\033[92m{self.get_log_prefix()}\033[0m-> connection opened at {timestamp}')
        self.subscribe()

    def on_close(self, _ws, status_code, close_msg) -> None:
        """Handles WebSocket closure and attempts reconnection."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\033[91m{self.get_log_prefix()}\033[0m-> connection closed at {timestamp}: '
              f'status {status_code}, message {close_msg}')

        if self.last_open_time and (time.time() - self.last_open_time) >= 5:
            print(f"\033[93m{self.get_log_prefix()}\033[0m-> Reconnecting WebSocket in 3 seconds...")
            time.sleep(3)
            self.start()

    def create_websocket(self) -> WebSocketApp:
        """Creates and returns a WebSocketApp instance."""
        print(f'\033[92m{self.get_log_prefix()}\033[0m-> creating WebSocket instance for {self.url}')
        self.ws = WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_message=self.on_message,
            on_error=self.on_error,
        )
        return self.ws

    def start(self):
        """Initializes and starts the WebSocket connection."""
        while True:
            try:
                self.ws = self.create_websocket()
                self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            except Exception as e:
                print(f'\033[91m{self.get_log_prefix()}\033[0m-> connection failed, retrying in 3 seconds... {e}')
                time.sleep(3)

    def on_message(self, _ws, message) -> None:
        """Handles incoming WebSocket messages (to be implemented in subclasses)."""
        raise NotImplementedError

    def subscribe(self):
        """Sends subscription request (to be implemented in subclasses)."""
        raise NotImplementedError

    def get_log_prefix(self) -> str:
        """Returns log prefix (to be implemented in subclasses)."""
        raise NotImplementedError
