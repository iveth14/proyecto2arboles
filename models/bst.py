from collections import deque
from .nodo import Nodo


class BST:

    def __init__(self):
        self.raiz = None


    def insertar(self, valor):
        nuevo = Nodo(valor)
        camino = []


        if self.raiz is None:
            self.raiz = nuevo
            camino.append(self.raiz)
            return camino
        

        cola = deque([self.raiz])
        while cola:
            actual = cola.popleft()
            camino.append(actual)

            if actual.izquierdo is None:
                actual.izquierdo = nuevo
                camino.append(nuevo)
                return camino
            else:
                cola.append(actual.izquierdo)  
        
            if actual.derecho is None:
                actual.derecho = nuevo
                camino.append(nuevo)
                return camino
            
            else:
                cola.append(actual.derecho)

        return camino
    
    def buscar(self, valor):
        camino = []
        if self.raiz is None:
            return False, camino 
        
        cola = deque([self.raiz])
        while cola:
            actual = cola.popleft()
            camino.append(actual)

            if actual.valor == valor:
                return True, camino
            
            if actual.izquierdo:
                cola.append(actual.izquierdo)
            if actual.derecho:
                cola.append(actual.derecho)

        return False, camino
    

    def eliminar(self, valor):
        if self.raiz is None:
            return False
        
        cola = deque([self.raiz]) 
        objetivo = None 
        ultimo = None
        padre_ultimo = None   
        es_hijo_izq = None

        while cola:
            actual = cola.popleft()

            if actual.valor == valor:
                objetivo = actual
            
            if actual.izquierdo:
                padre_ultimo = actual
                ultimo = actual.izquierdo
                es_hijo_izq = True
                ultimo = actual.izquierdo
                cola.append(actual.izquierdo)
            
            if actual.derecho:
                padre_ultimo = actual
                es_hijo_izq = False
                ultimo = actual.derecho
                cola.append(actual.derecho)

        if objetivo is None:
            return False
        
        if ultimo is None:
            self.raiz = None
            return True
        
        objetivo.valor = ultimo.valor
        if es_hijo_izq:
            padre_ultimo.izquierdo = None
        else:
            padre_ultimo.derecho = None
        return True
    

      