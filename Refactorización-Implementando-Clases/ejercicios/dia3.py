class Mapa:
    def __init__(self, filas, columnas, valor):
        self._filas = filas
        self._columnas = columnas
        self._matriz = [[valor] * columnas for a in range(filas)]

    def imprimir(self):
        for fila in self._matriz:
            row= ""
            for celda in fila:
                row += ("".join(str(celda)))
            print(row)
        
        print("\n")

    def coordenadas_validas(self, x, y):
        return 0 <= x < self._filas and 0 <= y < self._columnas
    
    def encontrar(self, tipo):
        for x in range(self._filas):
            for y in range(self._columnas):
                if isinstance(self._matriz[x][y], tipo):
                    return (x, y)
        return None
    
    def obtener_vecinos(self, x, y):
        direcciones = [(0,1), (1,0), (0,-1), (-1,0)]
        vecinos = []

        for dx, dy in direcciones:
            if self.coordenadas_validas(x+dx, y+dy):
                vecinos.append((x+dx, y+dy))
        return vecinos


    
    def actualizar_celda(self, x,y, valor):
        if self.coordenadas_validas(x,y):
            self._matriz[x][y] = valor
        else:
            print("Las coordenadas brindadas están fuera de la matriz")



class Celda:
    def __str__(self):
        return "? "
    
class Libre(Celda):
    def __str__(self):
        return ". "

class Muro(Celda):
    def __str__(self):
        return "# "

class Inicio(Celda):
    def __str__(self):
        return "P "

class Salida(Celda):
    def __str__(self):
        return "S "
    

def main():
    mi_mapa = Mapa(5,5, Libre())
    mi_mapa.imprimir()

    mi_mapa.actualizar_celda(0,0, Inicio())
    mi_mapa.actualizar_celda(4,4, Salida())
    mi_mapa.imprimir()

    mi_mapa.actualizar_celda(2,2, Muro())
    mi_mapa.actualizar_celda(2,3, Muro())
    mi_mapa.imprimir()

    inicio =mi_mapa.encontrar(Salida)
    print(inicio)

    vecinos = mi_mapa.obtener_vecinos(*inicio)
    print(vecinos)

main()

