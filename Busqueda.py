#-*- coding: utf-8 -*-
"""
Programador: Martínez Alfaro Felipe de Jesús.

Este programa está hecho para poder calcular los arboles generados por la busqueda por
anchura y altura.

                        #
                                #
                                            #
                                                        #
                                                                            #
"""

"""________________________________________________________________________________________"""
"""|                                       Blibliotecas                                   |"""
"""________________________________________________________________________________________"""
from re import S
from vaporGraph import *;

class Arbol(Grafo):
    def __init__(self,
                 algoritm,                  # 0 = BFS.
                 grafo:Grafo,               # Objeto Grafo, del que se va a sacar el arbol.
                 nodo_s,                    # Objeto nodo o el ID entero del nodo.
                 g_copy:bool=False,         # True si se quiere evitar modificar el grafo original.
                 id='A',                    # Nombre del grafo.
                 dirigido: bool = True,     # Indica si es o no el arbol dirigido.
                 ) -> None:
        super().__init__(id, 0, dirigido, False, None)  # Inicializo el grafo que representa el árbol.
        if g_copy: grafo = grafo.deepCopy();
        if algoritm == 0 or algoritm == "BFS":
            self.BFS(grafo,nodo_s)
        elif algoritm ==0 or algoritm == "DFS_R":
            self.DFS_R(grafo,nodo_s)
        else:
            self.DFS_I(grafo,nodo_s)




    def BFS(self,G:Grafo,s):
        # Por si s es un objeto o índice...
        getNodo = lambda t: G.nodos[t] if type(t) == int else t;
        l_i = [getNodo(s)]      # El nivel 0 respecto a s.
        l_i[0].val = l_i[0].A   # Copio las conecciones originales.
        l_i[0].A = Arista()     # Creo nuevas conecciones.
        self.addVert(l_i[0],True)
        while l_i != []:        # Hasta que ya todos los nodos alcanzables hallan sido ingresados.
            l_j = []            # L_i+1.
            for x in l_i:       # Para todo nodo a distancia i.
                for v in x.val:   # Para cada vector v que pertenece a la relación xRv.
                    if v in self: continue  # Si ya ha sido explorado.
                    v.val = Arista(v.A)     # Copia las aristas a las que originalmente estaba conectado.
                    v.A = Arista()          # Limpio las conecciones, ya que serán las del arbol.
                    x.add(v)                # Agrego la arista (x,v)
                    l_j.append(v)           # Agrego v a L_i+1
                    self.addVert(v,True)    # Agrego v a los vertices del Árbol
            l_i = l_j           # Me muevo a la siguiente lista.
        return self;

    # Crea un árbol a partil de un grafo, por medio de la búsqueda en profundidad recursiva.
    def DFS_R(self,G:Grafo,s):
        s = G.nodos[s] if type(s) == int else s;
        s.val = Arista(s.A)     # Copio las conecciones originales.
        s.A = Arista()          # Inicializo nuevas aristas.
        self.addVert(s,True)    # Añado el vertice al árbol.
        for v in s.val:         # Para cada vertice conectado a s.
            if v in self: continue          # Si ya ha sido explorado.
            s.add(v)            # Añado el vertice al grafo.
            self.DFS_R(G,v)     # Se llama a sí misma la fuoncióm.
        return self;

    # Crea un árbol a partir de un grafo, por medio de la búsqueda en profundidad iterativa
    def DFS_I(self,G:Grafo,s):
        s = G.nodos[s] if type(s) == int else s;
        v = s                   # El vertice a explorar.
        v.val = v               # Indíco que es el padre inicial.
        pila = []               # Pila para manejar los veetices a explorar.
        while True:             # Do while.
            if v.val != True:   # Así sé que ya están explorados.
                self.addVert(v,True)        # Añado v al árbol.
                for x in v.A:   # Para cada nodo relacionado con sus aristas salientes.
                    if x.val == True: continue          # Si ya está explorado lo salta.
                    x.val = v   # El padre en el arbol ahora será v.
                    pila.append(x)                      # Lo agrego a la pila para explorarlo.
                v.A = Arista()  # Limpio las aristas de v para hacer las del árbol.
                if v.val != v:  # Si no es el primer nodo.
                    v.val.add(v)# Añado la arista (v padre,v)
                v.val = True    # Indico que ya está explorado.
            if pila == []: break# while()
            v = pila.pop()      # voy a explorar el siguiente en la pila.
        return self;










if __name__ == "__main__":
    G = Grafo(dirigido=True).gnm()
    print(G)
    print(Arbol("BFS",G,0))
    #print(Arbol("DFS_R",G,0,True))
    #print(Arbol("DFS_I",G,0,True))

