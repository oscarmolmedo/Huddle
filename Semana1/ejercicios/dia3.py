###################################
####AGREGAMOS FUNCIONES DE DIA1 y DIA2####
####PARA IMPRIMIR, GENERAR MAPA y CALCULAR VECINOS VALIDOS####

def generar_mapa(filas, columnas):
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

def vecinos_validos(mapa, nodo):
    fila, columna = nodo
    
    #Movimientos en base a coordenada actual proporcionada
    posibles_vecinos =[
        (fila-1 , columna),         #IZQUIERDA
        (fila+1 , columna),         #DERECHA
        (fila , columna-1),         #ARRIBA
        (fila , columna+1),         #ABAJO
    ]

    #Se inicializa lista de vecinos validos
    vecinos_validos = []

    #Evaluamos coordenadas, validas dentro del tablero y que sea camino libre(0)
    for f, c in posibles_vecinos:                           #calcular f, c en base a coordenadas
        if 0 <= f < len(mapa) and 0 <= c < len(mapa[0]):
            if mapa[f][c] == 0:                             #si es camino libre
                vecinos_validos.append((f, c))
    return vecinos_validos

def construir_camino_corto(nodo, padres):
        camino = []
        while nodo is not None:
            camino.append(nodo)
            nodo = padres[nodo]
        
        camino.reverse()
        return camino

##################################
##################################

###IMPLEMENTACION DE BFS CON COLA

###
from collections import deque

def bfs(mapa, inicio, destino):
    cola = deque()
    cola.append(inicio)

    visitados = set()
    visitados.add(inicio)

    padres = {inicio: None}

    while cola:

        actual = cola.popleft()

        if actual == destino:
            break

        for vecino in vecinos_validos(mapa,actual):
            if vecino not in visitados :
                cola.append(vecino)
                visitados.add(vecino)
                padres[vecino] = actual
    
    if destino not in padres:
        return None
    
    
    return construir_camino_corto(destino, padres)

def marcar_camino(mapa, camino,inicio, destino):
    for (f, c) in camino:
        if (f, c) not in inicio and destino:
            mapa[f][c] = 3


mapa = generar_mapa(5,5)

x , y = len(mapa)-1, len(mapa[0])-1
nodo=(0,0)
destino=(x,y)
#vecinos = vecinos_validos(mapa, nodo)
mapa[1][0] = 1
mapa[1][1] = 1

mapa[2][3] = 1
mapa[3][2] = 1


imprimir_mapa(mapa)
print(f"\n")
camino = bfs(mapa,nodo,destino)
if camino:
    marcar_camino(mapa, camino,nodo, destino)
    imprimir_mapa(mapa)
else:
    print("No hay ruta")

print(camino)