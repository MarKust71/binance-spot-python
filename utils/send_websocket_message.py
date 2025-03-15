"""
This module contains a function that sends a message to the WebSocket server.
"""
import websocket

from db.utils.serialize_data import serialize_data


def send_websocket_message(message_data, error_message: str) -> None:
    """
    Send a message to the WebSocket server.
    :param message_data:
    :param error_message:
    :return:
    """
    try:
        ws = websocket.create_connection("ws://127.0.0.1:8000/ws")
        ws.send(serialize_data(message_data))
        ws.close()
    except ConnectionRefusedError:
        print(error_message)
