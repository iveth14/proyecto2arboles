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


