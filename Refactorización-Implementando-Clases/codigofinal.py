from collections import deque

####################################
####Definición de tipo de celdas####
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

        self.filas =       filas
        self.columnas =    columnas
        self.matriz =      [[valor] * columnas for a in range(filas)]


    def imprimir(self):

        for fila in self.matriz:
            row= ""
            for celda in fila:
                # row +=      ("".join(str(celda)))
                row +=      str(celda)
            print(row)
        
        print("\n")


    def coordenadas_validas(self, x, y):

        return 0 <= x < self.filas and 0 <= y < self.columnas
    
    
    # def encontrar_celda_portipo(self, tipo):

    #     for x in range(self.filas):
    #         for y in range(self.columnas):
    #             if isinstance(self.matriz[x][y], tipo):
    #                 return (x, y)
                
    #     return None
    
    
    def obtener_celda(self, x,y):

        if self.coordenadas_validas(x,y):
            return self.matriz[x][y]
        
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
            self.matriz[x][y] = valor
            return True
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
    def __init__(self, mapa, inicio, salida):

        self.mapa = mapa
        # self.inicio = mapa.encontrar_celda_portipo(Inicio)
        # self.salida = mapa.encontrar_celda_portipo(Salida)
        self.inicio = inicio
        self.salida = salida


    def buscar(self):

        if not self.inicio or not self.salida:
            print("Inicio o salida no están definidos en el mapa")
            
            return None
        
        padres = self._bfs()
        if not padres or self.salida not in padres:
            
            return None
        
        return self._construir_camino(padres)
    
    def _bfs(self):

        cola = deque([self.inicio])
        visitados = set([self.inicio])
        padres = {self.inicio:None}

        while cola:
            actual = cola.popleft()
            if actual == self.salida:
               
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
        nodo = self.salida

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



