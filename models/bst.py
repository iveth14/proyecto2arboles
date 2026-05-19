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
        
    def eliminar(self, valor):
        self.raiz, eliminado = self._eliminar(self.raiz, valor)
        return eliminado
    
    def _eliminar(self, nodo, valor):
        if nodo is None:
            return nodo, False
        
        eliminado = False

        if valor < nodo.valor:
            nodo.izquierdo, eliminado = self._eliminar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho, eliminado = self._eliminar(nodo.derecho, valor)
        else:
            eliminado = True
            if nodo.izquierdo is None and nodo.derecho is None:
                return None, eliminado
            if nodo.derecho is None:
                return nodo.izquierdo, eliminado
            
            sucesor = self._minimo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho, _ = self._eliminar(nodo.derecho, sucesor.valor)
        
        return nodo, eliminado
    

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado
    
    def _preorden(self, nodo, resultado):
        if nodo is None:
            return
        resultado.append(nodo)
        self._preorden(nodo.izquierdo, resultado)
        self._preorden(nodo.derecho, resultado)

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo is None:
            return
        self._inorden(nodo.izquierdo, resultado)
        resultado.append(nodo)
        self._inorden(nodo.derecho, resultado)

    def postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado
    
    def _postorden(self, nodo, resultado):
        if nodo is None:
            return
        self._postorden(nodo.izquierdo, resultado)
        self._postorden(nodo.derecho, resultado)
        resultado.append(nodo)

    def _minimo(self, nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo
    
    def altura(self):
        return self._altura(self.raiz)
    
    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
    
    def contar_nodos(self):
        return self._contar_nodos(self.raiz)
    
    def _contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_nodos(nodo.izquierdo) + self._contar_nodos(nodo.derecho)
    def limpiar(self):
        self.raiz = None

    def tipo(self):
        return "BST"

