#bst pe
from models.nodo import Nodo


class BST:

    def __init__(self):
        self.raiz = None


    def insertar(self, valor):
        camino = []
        self.raiz = self._insertar(self.raiz, valor, camino)
        return camino

    def _insertar(self, nodo, valor, camino):
        if nodo is None:
            nuevo = Nodo(valor)
            camino.append(nuevo)
            return nuevo
                
            camino.append(nodo)

        if valor < nodo.valor:
            nodo.izquierdo = self._insertar(nodo.izquierdo, valor, camino)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar(nodo.derecho, valor, camino)

        return nodo
    

    def buscar(self, valor):
        camino = []
        encontrado = self._buscar(self.raiz, valor, camino)
        return encontrado, camino
    
    def _buscar(self, nodo, valor, camino):
        if nodo is None:
            return False
        
        camino.append(nodo)

        if nodo.valor == valor:
            return True
        elif valor < nodo.valor:
            return self._buscar(nodo.izquierdo, valor, camino)
        else:
            return self._buscar(nodo.derecho, valor, camino)