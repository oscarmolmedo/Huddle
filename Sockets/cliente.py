import socket

cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli_socket.connect(("130.10.10.94", 5000))

cli_socket.sendall(b"HOLA")


cli_socket.close()