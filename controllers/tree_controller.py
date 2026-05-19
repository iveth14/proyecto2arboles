from models.bt import BT
from models.bst import BST
from models.avl import AVL
from utils.file_manager import FileManager


class TreeController:

    TIPOS = {"BT": BT, "BST": BST, "AVL": AVL}

    def __init__(self):
        self.arbol = BST()
        self._on_tree_changed = None
        self._on_animation = None
        self._on_message = None

    def set_on_tree_changed(self, fn):
        self._on_tree_changed = fn

    def set_on_animation(self, fn):
        self._on_animation = fn

    def set_on_message(self, fn):
        self._on_message = fn

    def cambiar_tipo(self, tipo):
        cls = self.TIPOS.get(tipo)
        if cls is None:
            self._msg(f"Tipo desconocido: {tipo}", "error")
            return
        self.arbol = cls()
        self._msg(f"Arbol cambiado a {tipo}", "info")
        self._notify()

    def insertar(self, valor):
        try: 
            v = int(valor)
        except ValueError:
            self._msg("debe ingresar un valor entero", "error")
            return
        camino = self.arbol.insertar(v)
        self._animate(camino)
        self._notify()
        self._msg(f"Valor {v} insertado", "success")

    def buscar(self, valor):
        try: 
            v = int(valor)
        except ValueError:
            self._msg("debe ingresar un valor entero", "error")
            return
        encontrado, camino = self.arbol.buscar(v)
        self._animate(camino)
        if encontrado:
            self._msg(f"Valor {v} encontrado, Nodos visitados: {len(camino)}")
        else:
            self._msg(f"Valor {v} no encontrado, Nodos visitados: {len(camino)}")

    def eliminar(self, valor):
        try: 
            v = int(valor)
        except ValueError:
            self._msg("debe ingresar un valor entero", "error")
            return
        eliminado = self.arbol.eliminar(v)
        self._notify()
        if eliminado:
            self._msg(f"Valor {v} eliminado")
        else:
            self._msg(f"Valor {v} no encontrado para eliminar")
        self._notify()
    
    def recorrer(self, tipo):
        metodos = {"preorden": self.arbol.preorden, "inorden": self.arbol.inorden, "postorden": self.arbol.postorden}

        fn = metodos.get(tipo)
        if fn is None:
            self._msg(f"Recorrido desconocido: {tipo}", "error")
            return
        
        nodos = fn()
        self._animate(nodos)
        valores = [str(n.valor) for n in nodos]
        self._msg(f"{tipo.capitalize()} recorrido: " + ", ".join(valores))


    def limpiar(self):
        self.arbol.limpiar()
        self._notify()
        self._msg("Arbol limpiado")

    def info(self):
        raiz_val = self.arbol.raiz.valor if self.arbol.raiz else "None"
        return {"tipo": self.arbol.tipo(), "altura": self.arbol.altura(), "raiz": raiz_val, "nodos": self.arbol.contar_nodos()}
    
    def guardar(self, ruta):
        okay = FileManager.guardar(self.arbol, ruta)
        if okay:
            self._msg(f"Arbol guardado en {ruta}", "success")
        else:
            self._msg(f"Error al guardar arbol en {ruta}", "error")

    def cargar(self, ruta):
        tipo, valores = FileManager.cargar(ruta)
        if tipo is None:
            self._msg(f"Error al cargar arbol desde {ruta}", "error")
            return
        self.cambiar_tipo(tipo)
        for v in valores:
            self.arbol.insertar(v)
        self._notify()
        self._msg(f"Arbol cargado es tipo {tipo} con {len(valores)} nodos")

    def _notify(self):
        if self._on_tree_changed:
            self._on_tree_changed()

    def _animate(self, camino):
        if self._on_animation and camino:
            self._on_animation(camino)
    def _msg(self, texto, tipo="info"):
        if self._on_message:
            self._on_message(texto, tipo)
    def get_raiz(self):
        return self.arbol.raiz