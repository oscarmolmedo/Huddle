from collections import deque

####################################
####Definición de tipó de celdas####
####################################
'''Celda es padre de las demás, se utiliza la herencia para poder centralizar cada clase hija como objeto 
y en un futuro poder agregar atributos a esta.'''
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
    
class Camino(Celda):
    def __str__(self):
        return "* "
    
##################
####Clase Mapa####
##################
'''Mapa hace: "Esta clase se inicializa con filas, columnas y el estado inicial de las celdas
se espera recibir las dimensiones de la matriz y el contenido base de esta"

            imprimir:               Imprime
            coordenadas_validas:    Valida coordenadas ingresadas
            encontrar_tipo_celda:   Valida si la celda es muro, salida, Inicio
            obtener_celda:          Devuelve valor de celda, previamente validado
            obtener_vecinos:        Genera Vecinos validos
            actualizar_celda:       Actualiza valor de una celda'''

class Mapa:
    def __init__(self, filas, columnas, valor):

        self._filas =       filas
        self._columnas =    columnas
        self._matriz =      [[valor] * columnas for a in range(filas)]

    def imprimir(self):

        for fila in self._matriz:
            row= ""
            for celda in fila:
                row +=      ("".join(str(celda)))
            print(row)
        
        print("\n")

    def coordenadas_validas(self, x, y):

        return 0 <= x < self._filas and 0 <= y < self._columnas
    
    def encontrar_celda_portipo(self, tipo):

        for x in range(self._filas):
            for y in range(self._columnas):
                if isinstance(self._matriz[x][y], tipo):
                    return (x, y)
                
        return None
    
    def obtener_celda(self, x,y):

        if self.coordenadas_validas(x,y):
            return self._matriz[x][y]
        
        return None
    
    def obtener_vecinos(self, x, y):
        direcciones =       [(0,1), (1,0), (0,-1), (-1,0)]
        vecinos =           []

        for dx, dy in direcciones:
            if self.coordenadas_validas(x+dx, y+dy):
                vecinos.append((x+dx, y+dy))

        return vecinos


    
    def actualizar_celda(self, x,y, valor):

        if self.coordenadas_validas(x,y):
            self._matriz[x][y] = valor
        else:
            print("Las coordenadas brindadas están fuera de la matriz")


####################################
####Definición de tipó de celdas####
####################################
'''Buscador hace:   "Esta clase se inicializa con mapa, se espera recibir la matriz y con las coordenadas de 
inicio y salida a través de la clase Mapa"
            
            buscar:                 .Función principal,Valida que en mapa exista inicio y salida, calcula y marca el camino
            _bfs:                   Calcula y almacena coordenadas para el camino más corto
            _construir_camino:      Construye en base a diccionario padres el camino más corto
            marcar_camino:          Recibe lista de camino corto y a excepción de inicio y salida conforme a la lista actualiza valores de la matriz

            '''

class Buscador:
    def __init__(self, mapa):

        self.mapa = mapa
        self._inicio = mapa.encontrar_celda_portipo(Inicio)
        self._salida = mapa.encontrar_celda_portipo(Salida)

    def buscar(self):

        if not self._inicio or not self._salida:
            print("Inicio o salida no están definidos en el mapa")
            
            return None
        
        padres = self._bfs()
        if not padres or self._salida not in padres:
            
            return None
        
        return self._construir_camino(padres)
    
    def _bfs(self):

        cola = deque([self._inicio])
        visitados = set([self._inicio])
        padres = {self._inicio:None}

        while cola:
            actual = cola.popleft()
            if actual == self._salida:
               
                break

            for vecino in self.mapa.obtener_vecinos(*actual):
                celda = self.mapa.obtener_celda(*vecino)
                
                if vecino not in visitados and not isinstance(celda, Muro):
                    cola.append(vecino)
                    visitados.add(vecino)
                    padres[vecino] = actual
        
        return padres
    
    def _construir_camino(self, padres):

        camino = []
        nodo = self._salida

        while nodo is not None:
            camino.append(nodo)
            nodo = padres[nodo]
        camino.reverse()

        return camino
    
    def marcar_camino(self, camino):

        for (x,y) in camino:
            celda = self.mapa.obtener_celda(x,y)
            
            if not isinstance(celda, (Inicio, Salida)):
                self.mapa.actualizar_celda(x,y, Camino())



def main():
    #Se muestra e  inicializa mapa
    mi_mapa = Mapa(5,5, Libre())
    mi_mapa.imprimir()

    #Se define punto de inicio y salida
    mi_mapa.actualizar_celda(0,0, Inicio())
    mi_mapa.actualizar_celda(4,4, Salida())

    #Se establecen obstáculos y se muestra mapa
    mi_mapa.actualizar_celda(1, 0, Muro())
    mi_mapa.actualizar_celda(1, 1, Muro())
    mi_mapa.actualizar_celda(2, 1, Muro())
    mi_mapa.actualizar_celda(3, 1, Muro())
    mi_mapa.imprimir()

    #Se calcula el camino
    buscar = Buscador(mi_mapa)
    camino = buscar.buscar()

    #Se evalúa si existe el camino o no y se muestra respectivamente
    if camino:
        buscar.marcar_camino(camino)
        mi_mapa.imprimir()
    else:
        print("No hay camino hacia la salida")

    
main()