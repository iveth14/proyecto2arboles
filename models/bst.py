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
            return camino