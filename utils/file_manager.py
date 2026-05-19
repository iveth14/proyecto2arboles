import json
import os
from collections import deque


class FileManager:
    #clase que guardar y carga el arbol a un archivo json
    @staticmethod
    def guardar(arbol, ruta: str) -> bool:
        """Serializa el arbol y lo guarda. Devuelve True si funciono."""
        try:
            valores = FileManager._bfs_valores(arbol.raiz)
            datos = {
                "tipo": arbol.tipo(),
                "valores": valores
            }
            directorio = os.path.dirname(ruta)
            if directorio:
                os.makedirs(directorio, exist_ok=True)

            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2)
            return True
        except Exception as e:
            print(f"[FileManager] Error al guardar: {e}")
            return False

    @staticmethod
    def cargar(ruta: str):
        """Carga un arbol desde un archivo JSON.
        Devuelve (tipo, valores) o (None, None) si hay error.
        """
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
            tipo = datos.get("tipo", "BST")
            valores = datos.get("valores", [])
            return tipo, valores
        except Exception as e:
            print(f"[FileManager] Error al cargar: {e}")
            return None, None

    @staticmethod
    def _bfs_valores(raiz) -> list:
        """Recorre el arbol nivel por nivel y devuelve lista de valores."""
        if raiz is None:
            return []
        resultado = []
        cola = deque([raiz])
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.valor)
            if nodo.izquierdo:
                cola.append(nodo.izquierdo)
            if nodo.derecho:
                cola.append(nodo.derecho)
        return resultado