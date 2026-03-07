import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.running = False

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)

    def handle_message(self, client_socket, data):
        """Lógica de procesamiento (Testeable unitariamente)"""
        if not data or not data.decode().strip():
            return False
        self.broadcast(data, client_socket)
        return True

    def client_thread(self, client_socket):
        while self.running:
            try:
                data = client_socket.recv(1024)
                if not self.handle_message(client_socket, data):
                    break
            except:
                break
        self.remove_client(client_socket)

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
            client.close()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"Servidor iniciado en {self.host}:{self.port}")
        
        while self.running:
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            threading.Thread(target=self.client_thread, args=(conn,), daemon=True).start()