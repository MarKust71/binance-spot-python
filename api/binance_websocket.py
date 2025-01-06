from api.handle_websocket_message import handle_websocket_message

import websocket


def on_error(ws, error):
    print('error', error)


def on_open(ws):
    print('connection opened')


def on_close(ws, status_code, close_msg):
    print(f'connection closed: status code: {status_code}, message: {close_msg}')


def on_message(ws, message):
    handle_websocket_message(message)


def ws_kline(url, symbol, interval):
    socket = f"{url}/ws/{symbol.lower()}@kline_{interval}"
    print(socket)

    return websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
