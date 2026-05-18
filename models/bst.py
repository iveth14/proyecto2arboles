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
    
