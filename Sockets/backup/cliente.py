import socket, os, threading, time

###PARA LIMPIAR EN CADA EJECUIÓN
os.system("cls")

def intentar_conexion (ip, puerto, reintentos=3, espera=2):

    for i in range(reintentos):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, puerto))

            return s
        
        except ConnectionRefusedError:
            print(f"Intento {i+1}/{reintentos}: servidor no disponible.")
            time.sleep(espera)
    
    return None

###POR CADA SALTO DE LÍNEA IMPRIME >>
def pretty_console():

    print(">> ", end="", flush=True)

def escuchar(sock):
    
    while True:
        try:
            data_in = sock.recv(4096)
            
            if not data_in:
                print("Conexion cerrada.")
                
                break
            
            ###MUESTRA CONVERSACINOES ENTRE CLIENTES
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
            send_comand = f"{tipo_A}{comando} ".encode()

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
                sock.sendall(send_comand)
                time.sleep(2)
                sock.close()
                break


            if comando == "nick":
                nuevo_nick = str(input("Ingrese su nuevo NICK: ")).encode()
                if len(nuevo_nick) >= 3:
                    set_nick = send_comand + nuevo_nick
                    print(set_nick)
                    sock.sendall(set_nick)
                    pretty_console()

                else:
                    print("Ingrese un nick con 3 carácteres como mínimo")
                    pretty_console()
        #Envia MSG
        else:
            mensaje = f"{tipo_B}{msg}".encode()
            sock.sendall(mensaje)
            pretty_console()
    
    #Cuando se ejecuta /exit
    return False
        

#BUCLE PRINCIPAL
while True:
    socket_client = intentar_conexion('130.10.10.94', 5000)

    ###Si no hay conexion exitosa rompe ciclo while
    if socket_client is None:
        print("No fue posible conectar con el servidor intente mas tarde")
        break
    
    ###CONECTA E INTENTA ENVIAR
    print("Conectado al servidor!")    
    threading.Thread(target=escuchar, args=(socket_client,),daemon=True).start()
    
    ###SI EL SERVER ESTA ABAJO AL ENVIAR REINTENTA
    try:
        e =enviar(socket_client)
        if e is False:
            break

    except Exception as e:
        print(f"Error en el cliente {e}\n")
    
    
    print(f"Desconectado del servidor. Intentando reconectar...\n")
