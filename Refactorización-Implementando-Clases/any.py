dimension_tablero= ()
from codigofinal import Mapa, Libre

while True:
    ingresar_dimension_tablero= input("Introduza dimension del tablero separado por ',' Ejemplo 5,5: ")
    es_tupla= tuple(map(int, ingresar_dimension_tablero.split(',')))
    if es_tupla:
        print(es_tupla)
        dimension_tablero += es_tupla
        break
    else:
        print("Introduzca números separados por ','")
print(dimension_tablero)

mi_mapa = Mapa(*dimension_tablero, Libre())
mi_mapa.imprimir()

