class Nodo:

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

        self.x = 0
        self.y = 0

    def __repr__(self):
        return f"Nodo({self.valor})"