import socket, os

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_socket.bind(("130.10.10.94", 5000))
srv_socket.listen(2)


a= srv_socket.accept()
print(a)
cli_socket, cli_addr = a

msg = cli_socket.recv(1024)



while True:
    if not msg:
        cli_socket.close()
        srv_socket.close()
        print("Cliente desconectado y cerrado")
        break
    else:
        #print(msg.decode())
        continue