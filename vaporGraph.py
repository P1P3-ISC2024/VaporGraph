#-*- coding: utf-8 -*-"""
"""
Programador: Martínez Alfaro Felipe de Jesús.

Este programa está hecho para poder manejar grafos, consta de 6 practicas
vistas en "Diseño y analisis de algoritmos".

                        #
                                #
                                            #
                                                        #
                                                                            #
"""

"""                                     BIBLIOTECAS                                 """
from ast import Return
from math import sqrt
import random
import string
from collections import UserDict
from unittest import skip
import copy

"""                                       CLASES                                    """

# Clase para manejar las aristas.
class Arista(dict):
    pass;

# Clase para el manejo de nodos, cada nodo gestiona sus aristas.
class Nodo:
    def __init__(self,id,dirigido:bool = False, ponderado:bool = False, valor=None) -> None:
        self.id = id            # Identificador del nodo.
        self.dir = dirigido     # Determina si pertenece a un grafo dirigido o no dirigido
        self.pond = ponderado   # ¿Sus aristas están ponderadas?
        self.padre = None;      # Guarda un registro de su antesesor en el caso de los árboles.
        self.val = valor        # Valor que se le desee darle a los nodos
        self.A = Arista()       # Diccionario Nodo: ponderación, si es grafo simple => ponderación = 0.
        pass;

    def copy(self):
        return copy.copy(self);

    def deepCopy(self):
        return copy.deepcopy(self);

    def __str__(self) -> str:
        if self.pond:           # para mostrar información más detallada
            des = ''
            for v in self.A:
                des += f"\n\t{self.id.__str__()}({self.val.__str__()})" # ID del saliente.
                des += f" -{'>' if self.dir else '-'} " # Flecha o linea.
                des += f"{v.id.__str__()}({v.val.__str__()});"       # ID del entrante.
            return des;
        des = f"\n\t{self.id} -{'>' if self.dir else '-'} "             # Imprime según es o no dirigido.
        des += '{'
        for v in self.A:                                # Para cada clave del diccionario.
            des += v.id.__str__() + ' '                 # El objeto id debe tener funcion __str__
        des += '};'
        return des;                                     # Debuelve toda la cadena.


    # Añade una arista ó actualiza el valor de una ya existente.
    def add(self,nodo,valor = 1) -> None:
        self.A[nodo] = valor;                           # Añade la clave o la rescribe.
        if not self.dir : nodo.A[self] = valor          # Solo si es no dirigido (doble sentido).
    pass;
    
    # Elmina la arista que se relaciona con un nodo.
    def cut(self,nodo) -> None:
        self.A.pop(nodo,None)                           # None es para que no devuelva error si no existe.
        if not self.dir: nodo.A.pop(self,None)          # Solo para no dirigidos.
        pass;

    # Indica si el nodo 'a' está conectado a 'b'
    def isConected(self,b) -> bool:
        return b in self.A;

    # Devuelve una lista de aristas que maneja en forma de tupla.
    def getAristas(self):
        E = []
        for nodo in self.A.keys():
            E.append( (self,nodo) )
        return E;

    # Devuelve una lista de aristas que maneja en forma de tupla usando el id de los objetos.
    def getDebugAristas(self):
        E = []
        for nodo in self.A.keys():
            E.append( (self.id,nodo.id) )
        return E;
    pass;


# Pila ponderada de vertices.
class PilaPond(list):
    # Inicializador.
    def __init__(init_list:list = []):
        super().__init__(init_list);
    # Meter un elemento.
    def append(self, v:Nodo) -> None:
        if len(self) == 0:
            self.insert(0,v)
            return 0;
        izq:int = 0                                     # Limite izquierdo de la búsqueda.
        der:int = len(self) - 1                         # Limite derecho de la búsqueda.
        while izq <= der:                               # Mientras no explore todo el array.
            i = izq + (der - izq)//2                    # i toma el valor de la mitad.
            if v.val >= self[i].val:                    # Si es el nodo buscado.
                self.insert(i+1,v)                      # Lo agrega después del nodo i.
                return 0;
            elif self[i].val < v.val:                   # Si el pibote está a ala izquierda del nodo.
                izq = i + 1                             # El limite izq ahora está a la der de i.
            else:
                der = i - 1                             # El limite der está a la izq de i.
        self.insert(i,v)
        return -1;                                      # Si no lo encuentra retorna -1.


# Clase grafo encargado de crear los nodos que se neciesiten y tenerlos en una lista acorde al ID.
class Grafo:
    def __init__(self,id='G', num_nodos:int = 10,dirigido:bool = False, ponderado:bool = False, init_valor=None) -> None:
        self.nodos = [Nodo(n,dirigido,ponderado,init_valor) for n in range(num_nodos)]  # Creo los nodos.
        self.card = len(self.nodos)                     # Cardinalidad o numero de nodos.
        self.id = id                                    # Identificador del grafo.
        self.dir = dirigido                             # Si es o no un grafo dirigido.
        self.pond = ponderado                           # Tiene ponderaciones?
        self.posibles = self.card**2 if self.dir else ((self.card-1)**2+(self.card-1))/2# La cantidad de aristas que pueden existir.
        pass;

    def __str__(self) -> str:
        descripcion = ("digraph " if self.dir else "graph ") + self.id.__str__() + " {"
        if self.pond:
            for nodo in self.nodos:
                descripcion += f"\n\t{nodo.id.__str__()}({nodo.val.__str__()})"
                #descripcion += f" [valor = {nodo.val.__str__()}];"
        for nodo in self.nodos:                         # Manda a expresar las aristas de cada nodo.
            descripcion += f"{nodo.__str__()}";
        descripcion += "\n}"                            # Cierra la descripción del grafo.
        return descripcion;                             # Retorna el string

    def copy(self):
        return copy.copy(self);

    def deepCopy(self):
        return copy.deepcopy(self);

    # Busca un nodo por su id, mediante busqueda binaria
    def searchNodo(self,v):
        izq:int = 0                                     # Limite izquierdo de la búsqueda.
        der:int = self.card - 1                         # Limite derecho de la búsqueda.
        while izq <= der:                               # Mientras no explore todo el array.
            i = izq + (der - izq)//2                    # i toma el valor de la mitad.
            if self.nodos[i].id == v.id:                # Si es el nodo buscado.
                return i;
            elif self.nodos[i].id < v.id:               # Si el pibote está a ala izquierda del nodo.
                izq = i + 1                             # El limite izq ahora está a la der de i.
            else:
                der = i - 1                             # El limite der está a la izq de i.
        return -1;                                      # Si no lo encuentra retorna -1.

    # Indica si la arista (a,b) existe, o si el nodo 'a' pertenece al grafo.
    def exist(self,a,b=None) -> bool:
        return b in a.A if b!=None else self.searchNodo(a) >= 0;   # La clave 'b' está en el diccinario de 'a'?

    # Sobrescribo el operador 'in' para usar con Aristas (tuplas) o nodos (clase Nodo), para saber si pertenece al grafo.
    def __contains__(self,item):
        return item[1] in item[0].A if type(item) != Nodo else self.searchNodo(item) >= 0;

    # Agrega un nodo al grafo.
    def addVert(self,v,by_id:bool=False):
        if (not by_id) or self.nodos == []:
            self.nodos.append(v)
        else:
            i=0
            while(i<self.card):
                if v.id <= self.nodos[i].id: break
                i += 1;
            self.nodos.insert(i,v)
        self.card = len(self.nodos)
        self.posibles = self.card**2 if self.dir else ((self.card-1)**2+(self.card-1))/2# La cantidad de aristas que pueden existir.
        return v;

    # Añade una arista al grafo.
    def addAri(self,a,b):
        a.add(b);

    # Ingresa un valor a todos los nodos del grafo.
    def setAll(self,valor,fun = None):
        if fun == None:
            for i in range(self.card):
                try:
                    self.nodos[i].val = valor.copy();   # Para que sus modif. sean indep.
                except AttributeError:
                    self.nodos[i].val = valor;          # Si no tiene función copy
        else:
            for i in range(self.card):
                self.nodos[i].val = fun(i,valor);
        return self;

    # Guarda el contenido del grafo.
    def save(self,nombre:str = "vapor", extension:str = ".gv"):
        # Validar que la extensión comience con punto.
        if not extension.startswith('.'):
            extension = '.' + extension
        # Construir el nombre completo del archivo
        nombre_archivo = nombre + extension
        # Escribir contenido en el archivo
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(self.__str__())
            print(f"Archivo guardado como: {nombre_archivo}")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
        return self;






    # Conecta un grafo gnm malla.
    def gnmalla(self, n:int = 10,m:int = 10):
        for i in range(self.card):
            #print(i,end = ' ')
            if i%n<n-1:         # Columnas.
                self.nodos[i].add(self.nodos[n*(i//n) + (i+1)%n])
                #                                j       i+1
            #else:
                #print('\n',end='')
            if i//n < m-1:      # Filas (j<m-1).
                self.nodos[i].add(self.nodos[n*((i+n)//n) + (i%n)])
                #                                j+1          i
            #print(f"{i} -> {i//n < m-1}")
            #print(f"\t + {n*( (i+n)//n ) + (i%n)}")
        return self;

    # Conecta un grafo a partir del modelo Erdős–Rényi.
    def gnm(self,m:int = 10):
        # Por si piden cosas raras xd...
        if( m > self.posibles ):
            print("No pueden existir tantas aristas diferentes!")
            return self;
        # Preparaciones para trabajar O(n^2)...
        V = self.nodos.copy()   # Nodos que tienen posiblidad de crear aristas.
        self.setAll(V,lambda i,valor:valor[:i] +valor[i+1:])                # Ingreso la posibilidad de conectar todos los nodos entre si.
        # Crea las m aristas O(m)...
        i:int = 0               # ninguna arista creada.
        while(i < m):
            # Eligo mis elmentos...
            a = random.choice(V)            # Elijo uno de los que tienen posibilidad.
            #print(f" {i}... {a.id}")
            #print(f"\t{a.id} -> {[n.id for n in a.val]}")
            b = random.choice(a.val)        # Elijo cualquier nodo posible a emparejar.
            #print("\t(",a,',',b,")")
            #print(f"\t{a.id} -> {[n.id for n in a.val]}")
            #print(f"\t{b.id} -> {[n.id for n in b.val]}")
            # Creo la arista...
            a.add(b)                        # Creo la arista.
            # Elmino la posibilidad de crear nuevamente esa arista...
            a.val.remove(b)                 # Elimino la posiblidad de (a,b)
            if not self.dir:    # Si es no dirigido,
                b.val.remove(a) # Elimino la posiblidad (b,a).
                if b.val == []: # Si ya no puede conectarse,
                    V.remove(b) # Elimina la posiblididad de ser elegido.
                    print([x.id for x in V])
            # Si ya no es posible crear más aristas con 'a'.
            if a.val == []:     # Si ya no es posible conectar con ningun nodo a 'a',
                V.remove(a)     # Elimino a 'a' de la lista de nodos con posibilidad.
                print([x.id for x in V])
            i += 1              # Indico que ya creé una arista.
        return self; # O(n^2+m) para tiempo, O(n^2) para espacio.

    # crea un grafo con el modelo Gn,p de Gilbert
    def gnp(self,p:float = 0.5):
        if (p > 1 or p <= 0):
            if p != 0:
                print("ERROR!! La probabilidad debe variar entre 0 y 1")
            return self;
        # Preparaciones para trabajar O(n^2)...
        V = self.nodos.copy()   # Nodos que tienen posiblidad de crear aristas.
        self.setAll(V,lambda i,valor:valor[:i] +valor[i+1:])                # Ingreso la posibilidad de conectar todos los nodos entre si.
        del V
        # Crea las m aristas O(m)...
        for v in self.nodos:
            for u in v.val:
                if random.random() <= p:
                    # Creo la arista...
                    v.add(u)                        # Creo la arista.
                    # Elmino la posibilidad de crear nuevamente esa arista...
                    v.val.remove(u)                 # Elimino la posiblidad de (v,u)
                    if not self.dir:    # Si es no dirigido,
                        u.val.remove(v) # Elimino la posiblidad (u,v).
        return self; # O(n^2)

    # Crea un grafo geografico simple.
    def gnr(self,r = 1,col:int = 2):
        fil = self.card//col -1             # Obtengo el numero de filas posibles.
        for vi in range(self.card):         # Para cada nodo.
            xi = vi%col         # Obtengo su posición en x.
            yi = vi//col        # Obtengo su posición en y.
            for vj in range(self.card):     # Reviso cada nodo si puede conectarse.
                xj = vj%col     # Obtengo su posición en x.
                yj = vj//col    # Obtengo su posición en x.
                if( r**2 < (xi-xj)**2 + (yi-yj)**2 ): continue              # Fuera del radio.
                if( (xi,yi) == (xj,yj) ): continue      # Es el mismo nodo.
                self.nodos[vi].add(self.nodos[vj])      # Lo conecto si cumple.
        return self;            # O(n^2)

    # Crea un grafo con el modelo Gnd Barabási-Albert
    def gnd(self,d:int = 1):
        # Verificaciones...
        if d == 1 or d > len(self.nodos):
            print("¡Valor no valido para d!")
            return self;
        # Conectamos los d nodos...
        for vi in self.nodos[:d]:
            for vj in self.nodos[:d]:
                if vi == vj: continue
                vi.add(vj)
                vi.val = len(vi.A)
                #print(vi.id,".",vi.val)
        # Calculo el numero de aristas...
        sk = d*(d-1) if self.dir else ((d-1)**2+(d-1))/2
        # Conectamos los nodos restantes...
        for vi in self.nodos[d:]:
            for vj in self.nodos[:vi.id]:
                pj = vj.val/sk
                if random.random() <= pj:
                    vi.add(vj)
                    sk += 1
                    vi.val += 1
        return self;

    # Crea un grafo con el modelo Gn Dorogovtsev-Mendes.
    def gn(self):
        n = self.card
        if n<3:
            print("Se requieren minimo 3 nodos para este algoritmo!!!")
            return self;
        for i in range(3):
            self.nodos[i].add(self.nodos[(i+1)%3])
        conteo = 3;
        triangulo = [ x.getAristas() for x in self.nodos[:3]]
        aristas = []
        for ar in triangulo:
            aristas += ar
        while(conteo<n):
            ari = random.choice(triangulo)[0]
            a = ari[0]
            b = ari[1]
            self.nodos[conteo].add(a)
            self.nodos[conteo].add(b)
            conteo += 1
        return self


    # Algoritmos de Dijkstra...
    def dijkstra(self,s):
        """
        Requiere que los nodos se inicialicen con None.
        """
        S = Grafo('S',0,self.dir,self.pond) # Grafo nuevo a generar.
        # Obtener el primer nodo de búsqueda
        getNodo = lambda t: self.nodos[t] if type(t) == int else t;
        pila = PilaPond()       # Pila ponderada (el de menor valor hasta arriba).
        actual = getNodo(s)     # Obtengo el nodo s.
        actual.val = 0          # Le pongo el valor 0 porque es el inicial.
        actual.padre = None     # Indico que no tiene padre.
        pila.append(actual)     # Lo agrego a la pila.
        actual = None           # Nungun seleccionado por el momento.
        # Ir recorriendo el grafo, según la pila...
        while pila:             # Mientras la pila no se vacie.
            # Selecciono el siguiente nodo...
            aux = pila.pop()    # Selecciono el sig en la pila.
            # Creo una copia con el valor original e indico al original que será explorado...
            aux2 = aux      # Uso aux2 como duplicado.
            aux = aux.copy()# Solo creo la copia.
            # Tratro los valores del elegido nodo para trabajar como el actual...
            aux.A = Arista()    # La copia ahora está desconectada.
            aux2.val = True # Altero el valor de visitado del original.
            # Trabajo con el nodo actual...
            if actual != None:  # Porque en el primer recorrido no hay actual.
                S.addVert(actual)           # Añado al nuevo grafo el nodo actual.
                aux.padre.add(aux) # Conecto el actual con el nodo elegido.
            actual = aux        # El nodo elegido ahora es el actual.
            for t in aux2.A:
                if t.val != True:           # Así sé que ya fue explorado y no lo tengo que buscar.
                    du = actual.val + aux2.A[t]      # d(u) + l_e (distancia entre el actual y la arista del nodo t)
                    if t.val == None:       # None == infinito
                        t.val = du          # Le pongo si o sí ese valor y quien se lo hereda.
                        t.padre = actual    # Le indico que su padre es el actual (su copia).
                        pila.append(t)      # Agrego ese nodo a la pila.
                    else:
                        if du < t.val:
                            t.padre = actual# asigno el padre que le herdará la minima.
                            t.val = du      # La minima dist. es la actual con la arista.
                        pila.append( pila.pop( pila.index(t) ) )            # Reordena el elemento en la pila.
        S.addVert(actual)           # Añado al nuevo grafo el nodo actual.
        return S;


    pass;










"""                                       FUNCIONES                                    """
# 1. Crea un grafo en forma de malla. Crea m*n nodos. Para el nodo ni,j crear una arista con el nodo ni+1,j y otra 
def gnmMalla(n:int = 2,m:int = 5,dirigido:bool=False,grafo_name="G",pon = True):
    """
    Genera grafo de malla
    :param m: número de columnas (> 1)
    :param n: número de filas (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n*m,dirigido,pon).gnmalla(n,m);

# 2. Crea un grafo a partir del modelo Erdős–Rényi. Crea n nodos y elegir uniformemente al azar m distintos pares de distintos vértices.
def gErdosRenyi(n_nodos:int = 10,m_aristas:int =10,dirigido:bool = False,grafo_name = "G",pon=True):
    """
    Genera grafo aleatorio con el modelo Erdos-Renyi
    :param n: número de nodos (> 0)
    :param m: número de aristas (>= n-1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n_nodos,dirigido,pon).gnm(m_aristas);

# 3. Modelo Gn,p de Gilbert. Crear n nodos y poner una arista entre cada par independiente y uniformemente con probabilidad p.
def gGilbert(n:int = 10, p:float = 0.5, dirigido=False,grafo_name="G",pon=True):
    """
    Genera grafo aleatorio con el modelo Gilbert
    :param n: número de nodos (> 0)
    :param p: probabilidad de crear una arista (0, 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n,dirigido,pon).gnp(p);

# 4. Modelo Gn,r geográfico simple. Colocar n nodos en un rectángulo unitario con coordenadas uniformes (o normales)
# y colocar una arista entre cada par que queda en distancia r o menor.
def gGeografico(n:int=10, r:int=3, dirigido=False,grafo_name="G",columnas:int = 2,pon = True):
    """
    Genera grafo aleatorio con el modelo geográfico simple
    :param n: número de nodos (> 0)
    :param r: distancia máxima para crear un nodo (0, 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n,dirigido,pon).gnr(r,columnas);

# 5. Variante del modelo Gn,d Barabási-Albert. Colocar n nodos uno por uno, asignando a cada uno d aristas a vértices distintos
# de tal manera que la probabilidad de que el vértice nuevo se conecte a un vértice existente v es proporcional a la cantidad de aristas que v tiene actualmente los primeros d vértices se conecta todos a todos.
def gBarabasiAlbert(n, d, dirigido=False, grafo_name = 'G',pon=True):
    """
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (> 0)
    :param d: grado máximo esperado por cada nodo (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n,init_valor=0,dirigido=dirigido,ponderado=pon).gnd(d);

# 6. Crea un grafo con Dorogovtsev-Mendes. Crear 3 nodos y 3 aristas formando un triángulo.
# Después, para cada nodo adicional, se selecciona una arista al azar y se crean aristas entre
# el nodo nuevo y los extremos de la arista seleccionada.
def gDorogovtsevMendes(n, dirigido=False,grafo_name = "G",pon = True):
    """
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (≥ 3)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n,dirigido,ponderado=pon).gn()

# Código que solo se ejecuta si este archivo se corre directamente.
if __name__ == "__main__":
    print(Grafo('G',9,False,True).gnmalla(3,3).dijkstra(0))#.save());
    # Resultados de malla...
    """gnmMalla(3,3).setAll(None).dijkstra(0).save("1_gnmMalla_Djk_9")
    gnmMalla(20,10,True).setAll(None).dijkstra(0).save("1_gnmMalla_Djk_200")"""
    #gnmMalla(20,25).save("1_gnmMalla_500")
    # Resultados de Erdős–Rényi...
    #gErdosRenyi(10,20).setAll(None).dijkstra(0).save("2_Erdos_Djk_10")
    #gErdosRenyi(200,400,True).setAll(None).dijkstra(0).save("2_Erdos_Djk_200")
    #gErdosRenyi(500,2000).save("2_Erdos_500")
    """# Resultados de Gilbert...
    gGilbert(10,0.3).setAll(None).dijkstra(0).save("3_Gilbert_Djk_10")
    gGilbert(200,0.3,True).setAll(None).dijkstra(0).save("3_Gilbert_Djk_200")
    #gGilbert(500,0.3).save("3_Gilbert_500")
    # Resultados de geográfico simple...
    gGeografico(10,5,False,'GS',5).setAll(None).dijkstra(0).save("4_GeoSimple_Djk_10")
    gGeografico(200,10,True,'GS',20).setAll(None).dijkstra(0).save("4_GeoSimple_Djk_200")
    #gGeografico(5000,12.5,False,'GS',20).save("4_GeoSimple_5000")
    # Resultados de Barabási-Albert..."""
    #gBarabasiAlbert(10,4).setAll(None).dijkstra(0).save("5_Albert_Djk_10")
    gBarabasiAlbert(200,4).setAll(None).dijkstra(0).save("5_Albert_Djk_200")
    #gBarabasiAlbert(500,4,True).save("5_Albert_500")
    # Resultados de Dorogovtsev-Mendes...
    #gDorogovtsevMendes(10).setAll(None).dijkstra(0).save("6_Dorogovtsev_Djk_10")
    gDorogovtsevMendes(200).setAll(None).dijkstra(0).save("6_Dorogovtsev_Djk_200")
    #gDorogovtsevMendes(500).save("6_Dorogovtsev_500")"""
    pass;
