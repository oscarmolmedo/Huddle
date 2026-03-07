# test_server.py
import pytest
from server import ChatServer

def test_handle_empty_message_returns_false():
    server = ChatServer()
    # Enviamos un string vacío
    result = server.handle_message("") 
    assert result is False # Esperamos que lo rechace