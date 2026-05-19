from models.bst import BST
from models.nodo import Nodo

class AVL(BST):


    def _h(self, nodo):
        return nodo.altura if nodo else 0
    
    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._h(nodo.izquierdo), self._h(nodo.derecho))

    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._h(nodo.izquierdo) - self._h(nodo.derecho)
    # Rotación 
    def _rotar_derecha(self, z):
        y = z.izquierdo
        T3 = y.derecho

        # Rotación
        y.derecho = z
        z.izquierdo = T3 

        # Actualizar alturas
        self._actualizar_altura(z)
        self._actualizar_altura(y)

        return y
    
    def _rotar_izquierda(self, z):
        y = z.derecho
        T2 = y.izquierdo

        # Rotación
        y.izquierdo = z
        z.derecho = T2

        # Actualizar alturas
        self._actualizar_altura(z)
        self._actualizar_altura(y)

        return y
    
    def _balancear(self, nodo):
        self._actualizar_altura(nodo)
        fb = self._factor_balance(nodo)

        if fb > 1 and self._factor_balance(nodo.izquierdo) >= 0:
            return self._rotar_derecha(nodo)
        
        if fb > 1 and self._factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        
        if fb < -1 and self._factor_balance(nodo.derecho) <= 0:
            return self._rotar_izquierda(nodo)
        
        if fb < -1 and self._factor_balance(nodo.derecho) > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        
        return nodo

    
