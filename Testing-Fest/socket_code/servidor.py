import socket, selectors, time, sys, os
sys.path.append(os.path.dirname(__file__))

from logic import procesar_protocolo, validar_nick, limpiar_mensaje


#lista de clientes
clientes = []
#diccionario socket-nick
nicks = {}

# Se crea el selector
sel = selectors.DefaultSelector()

def aceptar_conexion(sock):
    conn, addr = sock.accept()
    print(f"[+] Conectado: {addr}")
    conn.setblocking(False) #Sockes  no bloqueantes
    
    # Registramos el nuevo socket para lectura (EVENT_READ)
    # Usamos 'data' para guardar información extra si queremos
    sel.register(conn, selectors.EVENT_READ, data=addr)
    
    # Se carga en la listaw
    clientes.append(conn)
    nicks[conn] = None

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
    #cmd, arg = procesar_protocolo(contenido)
    cmd, arg = contenido.split(" ", 1)

    if cmd == "exit":
        print("Procesando comando...")
        time.sleep(1)
        desconectar_cliente(client_socket, client_addr)
        
        return False
    
    if cmd == "nick":
        if validar_nick(arg):
            nicks[client_socket]= arg
            print(f"{client_addr} ahora es {arg}")
            return True
        else:
            print(f"Nick rechazado para {client_addr}")
            return True
            

def leer_mensaje(conn, addr):
    try:
        msg = conn.recv(4096)
        if msg:
            data_decode = msg.decode()
            tipo, contenido = procesar_protocolo(data_decode)
            contenido = limpiar_mensaje(contenido)
            
            if tipo == "MSG":
                enviar_a_todos(conn, contenido)
                print(f">>> {nicks[conn]}: {contenido}")
            elif tipo == "CMD":
                procesar_comando(conn, addr, contenido)
        else:
            # Si no hay datos, es una desconexión limpia
            cerrar_conexion(conn, addr)
    except Exception:
        # Desconexión abrupta
        cerrar_conexion(conn, addr)

def cerrar_conexion(conn, addr):
    print(f"[-] Desconectando {addr}")
    sel.unregister(conn)
    desconectar_cliente(conn, addr)

# --- BUCLE PRINCIPAL  ---
def iniciar_servidor():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind(("127.0.0.1", 5000))
    lsock.listen()
    lsock.setblocking(False)    
    sel.register(lsock, selectors.EVENT_READ, data=None)

    print("SERVIDOR INICIADO")
    try:
        while True:
            eventos = sel.select(timeout=None) # Queda en escucha
            for key, mask in eventos:
                if key.data is None:
                    # Si no hay data, es el socket principal (nueva conexión)
                    aceptar_conexion(key.fileobj)
                else:
                    # Es un cliente existente con datos listos
                    leer_mensaje(key.fileobj, key.data)
    except KeyboardInterrupt:
        print("Cerrando servidor...")
    finally:
        sel.close()


if __name__ == "__main__":
    iniciar_servidor()