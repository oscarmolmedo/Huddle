
class Mapa:
    def __init__(self, filas, columnas):
        self._filas = filas
        self._columnas = columnas
        self._matriz = [[0] * columnas for a in range(filas)]

    def imprimir(self):
        for fila in self._matriz:
            row= ""
            for celda in fila:
                row += ". " if celda == 0 else "# "
            print(row)
        
        print("\n")

    def coordenadas_validas(self, x, y):
        return 0 <= x < self._filas and 0 <= y < self._columnas
    
    def actualizar_celda(self, x,y, valor):
        if self.coordenadas_validas(x,y):
            self._matriz[x][y] = valor
        else:
            print("Las coordenadas brindadas están fuera de la matriz")


def main():
    mi_mapa= Mapa(5,5)

    mi_mapa.imprimir()
    mi_mapa.actualizar_celda(4,4, 2)
    mi_mapa.imprimir()    


main()


    
