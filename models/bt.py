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
        return resultado

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
        return "BT"  
    