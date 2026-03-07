# server.py
class ChatServer:
    def handle_message(self, message):
        if not message.strip():
            return False
        return True