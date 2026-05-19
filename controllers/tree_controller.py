from models.bt import BT
from models.bst import BST
from models.avl import AVL
from utils.file_manager import FileManager


class TreeController:
    """Mediador entre la interfaz grafica y los modelos de arbol.

    La UI solo habla con el controlador.
    El controlador habla con los modelos y notifica a la UI
    mediante funciones callback registradas previamente.

    Callbacks disponibles:
    - on_tree_changed()        -> redibujar el arbol
    - on_animation(camino)     -> animar lista de nodos
    - on_message(texto, nivel) -> mostrar mensaje al usuario
    """

    TIPOS = {"BT": BT, "BST": BST, "AVL": AVL}

    def __init__(self):
        self.arbol = BST()          # arbol activo por defecto
        self._on_tree_changed = None
        self._on_animation = None
        self._on_message = None

    # --------------------------------------------------
    # Registro de callbacks
    # --------------------------------------------------
    def set_on_tree_changed(self, fn):
        self._on_tree_changed = fn

    def set_on_animation(self, fn):
        self._on_animation = fn

    def set_on_message(self, fn):
        self._on_message = fn

    # --------------------------------------------------
    # Cambio de tipo de arbol
    # --------------------------------------------------
    def cambiar_tipo(self, tipo: str):
        """Cambia el tipo de arbol y limpia la estructura."""
        cls = self.TIPOS.get(tipo)
        if cls is None:
            self._msg(f"Tipo desconocido: {tipo}", "error")
            return
        self.arbol = cls()
        self._msg(f"Arbol cambiado a {tipo}", "info")
        self._notify()

    # --------------------------------------------------
    # Operaciones principales
    # --------------------------------------------------
    def insertar(self, valor):
        try:
            v = int(valor)
        except ValueError:
            self._msg("Ingresa un numero entero valido.", "warning")
            return

        camino = self.arbol.insertar(v)
        self._notify()
        self._animate(camino)
        self._msg(f"Valor {v} insertado.", "success")

    def buscar(self, valor):
        try:
            v = int(valor)
        except ValueError:
            self._msg("Ingresa un numero entero valido.", "warning")
            return

        encontrado, camino = self.arbol.buscar(v)
        self._animate(camino)

        if encontrado:
            self._msg(f"Valor {v} encontrado. Nodos visitados: {len(camino)}", "success")
        else:
            self._msg(f"Valor {v} no encontrado. Nodos visitados: {len(camino)}", "warning")

    def eliminar(self, valor):
        try:
            v = int(valor)
        except ValueError:
            self._msg("Ingresa un numero entero valido.", "warning")
            return

        eliminado = self.arbol.eliminar(v)
        self._notify()

        if eliminado:
            self._msg(f"Valor {v} eliminado del arbol.", "success")
        else:
            self._msg(f"Valor {v} no existe en el arbol.", "warning")

    def recorrer(self, tipo: str):
        """Ejecuta un recorrido. tipo: 'preorden' | 'inorden' | 'postorden'"""
        metodos = {
            "preorden":  self.arbol.preorden,
            "inorden":   self.arbol.inorden,
            "postorden": self.arbol.postorden,
        }
        fn = metodos.get(tipo)
        if fn is None:
            self._msg(f"Recorrido desconocido: {tipo}", "error")
            return

        nodos = fn()
        self._animate(nodos)
        valores = [str(n.valor) for n in nodos]
        self._msg(f"{tipo.capitalize()}: {' -> '.join(valores)}", "info")

    def limpiar(self):
        self.arbol.limpiar()
        self._notify()
        self._msg("Arbol limpiado.", "info")

    # --------------------------------------------------
    # Informacion del arbol
    # --------------------------------------------------
    def info(self) -> dict:
        raiz_val = self.arbol.raiz.valor if self.arbol.raiz else "—"
        return {
            "tipo":   self.arbol.tipo(),
            "altura": self.arbol.altura(),
            "nodos":  self.arbol.contar_nodos(),
            "raiz":   raiz_val,
        }

    def get_raiz(self):
        return self.arbol.raiz

    # --------------------------------------------------
    # Persistencia
    # --------------------------------------------------
    def guardar(self, ruta: str):
        ok = FileManager.guardar(self.arbol, ruta)
        if ok:
            self._msg(f"Arbol guardado en {ruta}", "success")
        else:
            self._msg("Error al guardar el archivo.", "error")

    def cargar(self, ruta: str):
        tipo, valores = FileManager.cargar(ruta)
        if tipo is None:
            self._msg("Error al cargar el archivo.", "error")
            return
        self.cambiar_tipo(tipo)
        for v in valores:
            self.arbol.insertar(v)
        self._notify()
        self._msg(f"Arbol {tipo} cargado con {len(valores)} nodos.", "success")

    # --------------------------------------------------
    # Metodos internos
    # --------------------------------------------------
    def _notify(self):
        if self._on_tree_changed:
            self._on_tree_changed()

    def _animate(self, camino):
        if self._on_animation and camino:
            self._on_animation(camino)

    def _msg(self, texto, nivel="info"):
        if self._on_message:
            self._on_message(texto, nivel)