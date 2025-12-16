###################################
####AGREGAMOS FUNCIONES DE DIA1####
####PARA IMPRIMIR Y GENERAR MAPA###

def generar_mapa(columnas, filas):
    mapa = [
        [0] * columnas for a in range(filas)
    ]
    return mapa

def imprimir_mapa(mapa):

    for rows in mapa:
        row=""
        for celda in rows:
            if celda == 0:
                row += ". "             #camino libre
            elif celda == 1:
                row += "# "             #obstaculo pared
            elif celda == 2:
                row += "~ "             #obstaculo agua
            elif celda == 3:
                row += "* "             #camino corto
        print(row)

##################################
##################################

###IMPLEMENTACION DE BFS CON COLA

##OBTENER VECINOS VALIDOS
def vecinos_validos(mapa, nodo):
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


###FUNCION BFS con colas FIFO
from collections import deque
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

        for vecino in vecinos_validos(mapa,actual):        #Se genera vecinos validos, omite 
            if vecino not in visitados:                                      #Se no esta dentro de visitados se agrega a los contenedores
                cola.append(vecino)
                visitados.add(vecino)
                padres[vecino] = actual                             
    
    if destino not in padres:
        return None

    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = padres[nodo]
    
    camino.reverse()
    return camino



    

mapa = generar_mapa(3,3)


nodo=(0,0)
destino=(2,2)
vecinos = vecinos_validos(mapa, nodo)
mapa[1][0] = 1
mapa[1][1] = 1
mapa[2][1] = 1


imprimir_mapa(mapa)

calculate = bfs(mapa,nodo,destino)
print(calculate)

    