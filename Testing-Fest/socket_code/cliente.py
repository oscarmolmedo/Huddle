import socket, sys, selectors, os
from logic import validar_nick

sel = selectors.DefaultSelector()

def enviar_mensaje(sock):
    # Leemos de la entrada estándar (teclado)
    msg = sys.stdin.readline().strip()
    if not msg:
        return

    tipo_A = "CMD|"
    tipo_B = "MSG|"

    if msg.startswith("/"):
        comando = msg[1:].split(" ", 1)
        nombre_cmd = comando[0]
        
        if nombre_cmd == "exit":
            print("Saliendo...")
            sel.unregister(sock)
            sock.close()
            sys.exit()
            
        elif nombre_cmd == "nick":
            nuevo_nick = input("Ingrese su nuevo NICK: ")
            if validar_nick(nuevo_nick):
                payload = f"{tipo_A}nick {nuevo_nick}".encode()
                sock.sendall(payload)
            else:
                print("Nick inválido (mínimo 3 caracteres).")
    else:
        # Mensaje normal
        sock.sendall(f"{tipo_B}{msg}".encode())
    
    print(">> ", end="", flush=True)

def recibir_mensaje(sock):
    data = sock.recv(4096)
    if data:
        print(f"\n< {data.decode()}")
        print(">> ", end="", flush=True)
    else:
        print("\n[!] Conexión perdida con el servidor.")
        sel.unregister(sock)
        sock.close()
        sys.exit()

def iniciar_cliente(ip, puerto):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, puerto))
        sock.setblocking(False)
        print(f"Conectado a {ip}:{puerto}")
        print(">> ", end="", flush=True)

        # Registramos el socket para recibir mensajes
        sel.register(sock, selectors.EVENT_READ, data=recibir_mensaje)
        
        # Registramos la entrada estándar (teclado) para enviar mensajes
        # sys.stdin es el archivo que representa lo que escribes
        sel.register(sys.stdin, selectors.EVENT_READ, data=enviar_mensaje)

        while True:
            eventos = sel.select()
            for key, mask in eventos:
                callback = key.data
                callback(key.fileobj)
                
    except ConnectionRefusedError:
        print("Servidor no disponible.")
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
    finally:
        sel.close()

if __name__ == "__main__":
    os.system("cls")
    iniciar_cliente('127.0.0.1', 5000)