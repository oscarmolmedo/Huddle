
class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[0] * columnas for a in range(filas)]

    def imprimir(self):
        for fila in self.matriz:
            row= ""
            for celda in fila:
                row += ". " if celda == 0 else "# "
            print(row)
        
        print("\n")

    def actualizar_celda(self, x,y):
        self.matriz[x][y] = 1

def main():
    mi_mapa = Mapa(5,7)
    mi_mapa.imprimir()

    mi_mapa.actualizar_celda(0,0)
    mi_mapa.imprimir()