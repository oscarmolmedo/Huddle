from collections import deque
import os
import time

#####################
######FUNCIONES######
#####################

def limpiar_consola():
    os.system("cls")

def validar_input_coordenada(coordenadas, mapa):

    x, y = coordenadas

    if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]):
        if mapa[x][y] == 0:
            return True
        
    return False

def generar_mapa(filas, columnas):
    mapa = [
        [0] * columnas for a in range(filas)
    ]
    return mapa

def imprimir_mapa(mapa):

    for rows in mapa:                    #Itera sobre listas = fila 
        row=""
        for celda in rows:              #Itera sobre elementos de la lista = celda de la fila
            if celda == 0:
                row += ". "              #camino libre
            elif celda == 1:
                row +=          "# " #obstaculo edificio
            elif celda == 2:
                row +=          "~ " #obstaculo agua
            elif celda == 3:
                row +=          "* " #camino corto
            elif celda == 4:
                row +=          "P " #Punto de partida
            elif celda == 5:
                row +=          "S " #Salida
        print(row)

def calcular_vecinos_validos(mapa, nodo, destino):
    fila, columna = nodo
    
    #Movimientos en base a coordenada actual proporcionada
    vecinos =[
        (fila-1 , columna),         #IZQUIERDA
        (fila+1 , columna),         #DERECHA
        (fila , columna-1),         #ARRIBA
        (fila , columna+1),         #ABAJO
    ]

    #Se inicializa lista de vecinos validos
    vecinos_validos = []

    #Evaluamos coordenadas, validas dentro del tablero y que sea camino libre(0)
    for f, c in vecinos:                           #Toma f, c en base a coordenadas
        if 0 <= f < len(mapa) and 0 <= c < len(mapa[0]):
            if mapa[f][c] == 0 or (f,c) == destino:                             #si es camino libre
                vecinos_validos.append((f, c))
    return vecinos_validos

def construir_camino(nodo, padres):
        camino = []
        while nodo is not None:
            camino.append(nodo)
            nodo = padres[nodo]
        
        camino.reverse()
        return camino

def marcar_camino(mapa, camino,inicio, destino):
    for (f, c) in camino:                           #Crea camino en base a lista invertida retornada por contruir_camino
        if (f, c) not in inicio and destino:
            mapa[f][c] = 3

def bfs(mapa, inicio, destino):
    ###INICIALIZAMOS CONTENEDORES###
    cola = deque()
    cola.append(inicio)                                                     #Coordenada de inicio

    visitados = set()                                                       #Agrega vecinos visitados y no repite celdas visitadas
    visitados.add(inicio)                                                   #Se incluye coordenada de inicio

    padres = {inicio: None}                                                 #Diccionario padres

    #Bucle de ejecución
    while cola:

        actual = cola.popleft()                                             #Toma primer elemento de la cola
        if actual == destino:
            break

        for vecino in calcular_vecinos_validos(mapa,actual, destino):        #Se genera vecinos validos, omite 
            if vecino not in visitados:                                      #Se no esta dentro de visitados se agrega a los contenedores
                cola.append(vecino)
                visitados.add(vecino)
                padres[vecino] = actual                             
    
    if destino not in padres:                                               #Si no hay camino a destino
        return None
    
    
    return construir_camino(destino, padres)                                #Almacena y retorna lista invertida en orden


################
######MAIN######
################

def main():
    limpiar_consola()
    ###Definicion de dimensiones por usuario###
    while True:

        x = int(input("Establezca cantidad de filas: "))
        y = int(input("Establezca cantidad de columnas: "))


        if x < 15 and y < 15:
            posicion = x,y
            break
        else:
            print("Cantidad de filas y columas limitado a 15")
    
    ###Se muestra estado inicial del tablero###
    mapa = generar_mapa(posicion[0], posicion[1])
    limites_mapa = ((len(mapa)-1),(len(mapa[0])-1))

    print("Estado inicial del tablero")
    imprimir_mapa(mapa)
    print(f"\n")


    ###BLOQUE CON VALIDACIÓN PARA INSERTAR POR USUARIO COORDENADAS DE OBSTACULOS###
    ###############################################################################
    inicio = ()
    destino = ()

    while True:
        continuar = input("Desea agregar obstáculos?. Si para continuar No para finalizar: ").lower()
        if continuar == "si":

            while True:

                obstaculo = int(input("Seleccione: 1 para muros, 2 para agua, 3 para finalizar: "))
                
                if obstaculo in (1,2):

                    print("Establezca donde quiere colocar el obstáculo")
                    x = int(input("Introduza posicion x(fila): "))
                    y = int(input("Introduza posicion y(columna): "))

                    if validar_input_coordenada((x,y) , mapa):
                        mapa[x][y] = obstaculo
                        imprimir_mapa(mapa)
                        print(f"\n")
                    else:
                        print(f"Las coordendas deben de ser para x entre (0, {limites_mapa[0]}) y para y entre (0, {limites_mapa[1]})") 

                elif obstaculo == 3:
                    break
                else:
                    print("Seleccione 1 o 2 para obstaculos y 3 para finalizar")
        else:
            break        


    ###BLOQUE CON VALIDACIÓN PARA INSERTAR POR USUARIO COORDENADAS DE INICIO Y FIN###
    #################################################################################      
    while True:
            print("Establezca donde quiere iniciar")
            x = int(input("Introduza posicion x: "))
            y = int(input("Introduza posicion y: "))


            if validar_input_coordenada((x,y) , mapa):
                inicio = x,y
                mapa[x][y] = 4
            
                print(f"El punto de partida fue definido en {inicio}")
                imprimir_mapa(mapa)
                print(f"\n")

                break
            elif mapa[x][y] != 0:
                print(f"En {x,y} hay un obstáculo, eliga otra posición")
            else:
                print(f"Las coordendas deben de ser para x entre (0, {limites_mapa[0]}) y para y entre (0, {limites_mapa[1]})")

    while True:
            print("Establezca donde quiere finalizar")
            x = int(input("Introduza posicion x: "))
            y = int(input("Introduza posicion y: "))


            if validar_input_coordenada((x,y) , mapa):
                mapa[x][y] = 5
                destino = x,y

                print(f"La salida fue definida en {destino}")
                imprimir_mapa(mapa)
                print(f"\n")
                time.sleep(3)
                limpiar_consola()

                break
            elif mapa[x][y] != 0:
                print(f"En {x,y} hay un obstáculo, eliga otra posición")
            else:
                print(f"Las coordendas deben de ser para x entre (0, {limites_mapa[0]}) y para y entre (0, {limites_mapa[1]})")
    
    
    ###Bloque FINAL###
    ##################
    camino = bfs(mapa, inicio, destino)

    if camino:                                                  ###Si lista de camino existe, marca el camino corto
        marcar_camino(mapa, camino, inicio, destino)
        imprimir_mapa(mapa)
        print(f"El camino a seguir es {camino}")
    else:
        print("No hay camino posible en el mapa")

main()


