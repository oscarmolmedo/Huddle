
def generar_mapa(columnas, filas):
    mapa = [
        [0] * columnas for a in range(filas)
    ]
    return mapa

def imprimir_mapa(mapa):

    mapa_dimension= len(mapa)

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
                row += "x "             #camino corto
        print(row)


def in_coordenadas(mapa):

    while True:
        x = int(input("Ingrese nro fila: "))
        y = int(input("Ingrese nro de columna: "))
        
        coordenadas = x,y
        #len mapa total de filas y len mapa[] total de elementos de cualquiera de las filas o columnas
        if 0 <= coordenadas[0] < len(mapa) and 0 <= coordenadas[1] < len(mapa[0]):
            return coordenadas
        else:
            print("Las coordenadas estan fuera de los limites")
            continue
    
##Ejercio 1
##Estado incial tablero
# mapa1 = generar_mapa(5,5)
# imprimir_mapa(mapa1)

# #Ingreso de coordenadas y actualizacion de celda
# coodenadas1 = in_coordenadas(mapa1)
# fila, columna = coodenadas1
# mapa1[fila][columna] = 2
# imprimir_mapa(mapa1)

####Ejercio2
#Se inicializa tablero fuera del while para poder actualizarlo
mapa2 = generar_mapa(3,6)

while True:
    ##Solicitud de coordenadas con validacion interna
    imprimir_mapa(mapa2)
    coordenadas2 = in_coordenadas(mapa2)
    
    ##Bloque de insercion de obstaculos con verificacion
    print(f"Los obstaculos son:\n 1. Pared  2. Agua")
    obstaculo = int(input(f"Introduzca 1 o 2 para seleccionar el obstaculo: "))
    fila, columna = coordenadas2
    if obstaculo == 1 or obstaculo ==2:
        mapa2[fila][columna] = obstaculo
    else:
        print("Debe de introducir el numero 1 o 2 para los obstaculos")
    
    ##Condicion de continuidad definida por ususario
    continuar = input(f"Desea continuar?\n Si para continuar Fin para finalizar: ").lower()
    if continuar == "fin":
        break   
        
imprimir_mapa(mapa2)
    
