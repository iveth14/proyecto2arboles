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
    
    def insertar(self, valor):
        camino = []
        self.raiz = self._insertar(self.raiz, valor, camino)
        return camino
    
    def _insertar_avl(self, nodo, valor, camino):
        if nodo is None:
            nuevo = Nodo(valor)
            camino.append(nuevo)
            return nuevo
        
        camino.append(nodo)

        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_avl(nodo.izquierdo, valor, camino)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_avl(nodo.derecho, valor, camino)
        else:
            return nodo
        
        return self._balancear(nodo)
    
    def eliminar(self, valor):
        self.raiz, eliminado = self._eliminar_avl(self.raiz, valor)
        return eliminado
    
    def _eliminar_avl(self, nodo, valor):
        if nodo is None:
            return nodo, False
        
        eliminado = False

        if valor < nodo.valor:
            nodo.izquierdo, eliminado = self._eliminar_avl(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho, eliminado = self._eliminar_avl(nodo.derecho, valor)
        else:
            eliminado = True
            if nodo.izquierdo is None:
                return nodo.derecho, eliminado
            if nodo.derecho is None:
                return nodo.izquierdo, eliminado
            
            sucesor = self._minimo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho, _ = self._eliminar_avl(nodo.derecho, sucesor.valor)

        return self._balancear(nodo), eliminado
    
    def tipo(self):
        return "AVL"
    
    def info_balance(self):
        info = {}
        self._recorrer_balance(self.raiz, info)
        return info
    
    def _recorrer_balance(self, nodo, info):
        if nodo is None:
            return
        
        info[nodo.valor] = self._factor_balance(nodo)
        self._recorrer_balance(nodo.izquierdo, info)
        self._recorrer_balance(nodo.derecho, info)
