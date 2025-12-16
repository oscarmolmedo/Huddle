from codigofinal import Mapa, Libre, Inicio, Salida, Muro, Buscador
import os

def introducir_coordenadas():
    coordenadas= ()
    while True:

        ingresar_dimension_tablero= input(f"Introduzca las coordenadas separado por ',' Ejemplo 5,5: \n")
        es_tupla= tuple(map(int, ingresar_dimension_tablero.split(',')))

        if es_tupla:
            coordenadas += es_tupla
            break
        else:
            print(f"Introduzca números separados por ',' \n")
    
    return coordenadas


def main():

    os.system("cls")

    print("Introduzca dimensiones para tablero")
    dimension_tablero= introducir_coordenadas()


    #Se muestra e  inicializa mapa
    mi_mapa = Mapa(*dimension_tablero, Libre())
    mi_mapa.imprimir()


    #Se define punto de inicio y salida
    while True:

        print("Defina el Inicio en el mapa")
        inicio_mapa = introducir_coordenadas()


        introducir_inicio = mi_mapa.actualizar_celda(*inicio_mapa, Inicio())
        if introducir_inicio:
            break

    while True:

        print("Defina la Salida en el mapa")
        salida_mapa = introducir_coordenadas()


        introducir_salida = mi_mapa.actualizar_celda(*salida_mapa, Salida())
        if salida_mapa != inicio_mapa:
            if introducir_salida:
                break
        else:
            print("La salida es igual a la entrada, introduzca de nuevo")
            continue

    mi_mapa.imprimir()


    #Se establecen obstáculos y se muestra mapa
    while True:
        print(f"Ingrese coordenadas para introducir/quitar obstáculos: \n")
        obstaculo_mapa = introducir_coordenadas()
        print(f"Seleccione 1.Introducir 2. Quitar obstáculo: \n")


        accion_obstaculo =  int(input("1. Introducir 2. Quitar"))
        if accion_obstaculo == 2:
            mi_mapa.actualizar_celda(*obstaculo_mapa, Libre())
        elif accion_obstaculo ==1:
            mi_mapa.actualizar_celda(*obstaculo_mapa, Muro())
        else:
            print("Introduza 1 o 2 para realizar las acciones correspondientes")


        mi_mapa.imprimir()
        print("Desea introducir/quitar más obstáculos")
        continuar=str(input(f"Introduzca si o no: \n"))
        if continuar == "no" and len(continuar) == 2:
            break

    mi_mapa.imprimir()

    #Se calcula el camino
    buscar = Buscador(mi_mapa, inicio_mapa, salida_mapa)
    camino = buscar.buscar()

    #Se evalúa si existe el camino o no y se muestra respectivamente
    if camino:
        buscar.marcar_camino(camino)
        mi_mapa.imprimir()
    else:
        print("No hay camino hacia la salida")

    
main()