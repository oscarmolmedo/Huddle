import socket, os, threading, time
os.system("cls")


###INICIALIZACION###
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
socket_server.bind(("130.10.10.94", 5000))
socket_server.listen()                             #cantidad de clientes en cola

#lista de clientes
clientes = []
#diccionario socket-nick
nicks = {}

#PROCESAR DESCONEXION
def desconectar_cliente(client_sock, client_addr):

    if client_sock in clientes:
        clientes.remove(client_sock)

    if client_sock in nicks:
        print(f"Eliminando a {nicks[client_sock]} {client_addr}")
        del nicks[client_sock]
    
    try:
        client_sock.close()
    except:
        pass
  

#BROADCAST | REMITENTE ES CLIENTE_SOCKET
def enviar_a_todos(remitente, msg):

    nick_salida = f"{nicks.get(remitente)}: {msg}".encode()
    
    for c in clientes:
        if c != remitente:

            try:
                c.sendall(nick_salida)
            except:
                clientes.remove(c)
                c.close()

#EJECUTAR COMANDOS
def procesar_comando (client_socket, client_addr,contenido):

    ###Para separar comando de nombre<nick>
    cmd, arg = contenido.split(" ",1)

    if cmd == "exit":
        print("Procesando comando...")
        time.sleep(1)
        desconectar_cliente(client_socket, client_addr)
        
        return False
    
    if cmd == "nick":
        nicks[client_socket]= arg
        print(f"{client_addr} ahora es {arg}")

        return True
        
#TRATAR CONEXION CLIENTES
def manejar_cliente(client_sock, client_addr):

    while True:
        try:

            msg = client_sock.recv(4096)

            if not msg:
                print("[!] Desconexion detectada")
                if client_sock in clientes:
                    desconectar_cliente(client_sock, client_addr)
                break

            tipo, contenido = msg.decode().split("|",1)
            print('El contenido es',contenido)


            if tipo == "MSG":
                enviar_a_todos(client_sock, contenido)


            elif tipo == "CMD":
                continuar = procesar_comando(client_sock,client_addr ,contenido)
                if not continuar:
                    break

            print(f"{nicks[client_sock]}>>> {msg.decode()}")

        except (ConnectionResetError, ConnectionAbortedError) as e:
            print("[!] Cliente desconectado de forma abrupta.")
            print(e)

            desconectar_cliente(client_sock, client_addr)
            break


print("SERVIDOR INICIADO")

while True:

    client_socket, client_addr = socket_server.accept()
    print(f"[+] Cliente conectado {client_addr}")

    welcome_message = f"--|Bienvenido {client_addr} a MAIN_SERVER|-- \n### /help para ver comandos ###".encode()
    client_socket.send(welcome_message)

    clientes.append(client_socket)
    nicks[client_socket]= None

    hilo = threading.Thread(target=manejar_cliente, args=(client_socket,client_addr), daemon=True)
    hilo.start()

