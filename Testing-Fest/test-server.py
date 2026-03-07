# test_server.py
import pytest
from unittest.mock import MagicMock
from server import ChatServer

def test_process_message_rejects_empty():
    server = ChatServer()
    # Simulamos un socket que no envía nada
    mock_socket = MagicMock()
    
    # La función debe retornar False o lanzar un error si el mensaje es vacío
    result = server.handle_message(mock_socket, b"a") 
    assert result is True