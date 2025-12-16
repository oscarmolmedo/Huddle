import socket, os, threading, time

os.system("cls")

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
socket_client.connect(("130.10.10.94", 5000))

def pretty_console():

    print(">> ", end="", flush=True)

def escuchar(sock):
    while True:
        try:
            data_in = sock.recv(1024)
            if not data_in:
                print("Conexion cerrada.")
                break
            print("\n<", data_in.decode())
            pretty_console()
        except:
            break

def enviar(sock):
    while True:
        
        msg = input("")
        tipo_A = "CMD|"
        tipo_B = "MSG|"
        
        #ENVIA CMD
        if msg.startswith("/"):
            comando = msg[1:]
            s = f"{tipo_A}{comando} ".encode()

            if comando == "help":
                print("""
                Comandos disponibles:
                /nick        -  Agregar/Cambiar tu nick.
                /exit        -  Salir del chat.
                /help        -  Mostrar esta ayuda.
                """)
                pretty_console()
                continue

            
            if comando == "exit":
                sock.sendall(s)
                time.sleep(2)
                sock.close()
                break

            if comando == "nick":
                nuevo_nick = input("Ingrese su nuevo NICK: ").encode()
                set_nick = s + nuevo_nick
                sock.sendall(set_nick)
                pretty_console()
        #Envia MSG
        else:
            mensaje = f"{tipo_B}{msg}".encode()
            sock.send(mensaje)
            pretty_console()


threading.Thread(target=escuchar, args=(socket_client,),daemon=True).start()
enviar(socket_client)

