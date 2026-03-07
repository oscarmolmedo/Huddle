# test_integration.py
import socket
import threading
import pytest
import time
from server import ChatServer

@pytest.fixture
def running_server():
    server = ChatServer('127.0.0.1', 5005)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.1) # Damos tiempo a que el socket abra
    yield server
    server.running = False
    server.server_socket.close()

def test_client_connection_and_broadcast(running_server):
    # Cliente 1
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.connect(('127.0.0.1', 5005))
    
    # Cliente 2
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2.connect(('127.0.0.1', 5005))
    
    # Cliente 1 envía mensaje
    client1.send(b"")
    
    # Cliente 2 debería recibirlo
    data = client2.recv(1024)
    assert data == b"Hola a todos"
    
    client1.close()
    client2.close()