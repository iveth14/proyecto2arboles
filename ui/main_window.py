from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QComboBox,
    QGroupBox, QStatusBar, QFileDialog, QFrame, QTimer
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.tree_canvas import TreeCanvas

ESTILO = """
QMainWindow, QWidget {
    background-color: #0f1117;
    color: #e2e8f0;
    font-family: 'Segoe UI', sans-serif;
}
QGroupBox {
    border: 1px solid #1e293b;
    border-radius: 8px;
    margin-top: 10px;
    padding: 8px;
    font-weight: bold;
    color: #94a3b8;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}
QPushButton {
    background-color: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #263450;
    border-color: #38bdf8;
    color: #38bdf8;
}
QPushButton:pressed {
    background-color: #0ea5e9;
    color: #0f1117;
}
QPushButton#primario {
    background-color: #0369a1;
    border-color: #38bdf8;
    font-weight: bold;
}
QPushButton#peligro {
    background-color: #7f1d1d;
    border-color: #ef4444;
}
QLineEdit {
    background-color: #1e293b;
    color: #f1f5f9;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 13px;
}
QLineEdit:focus { border-color: #38bdf8; }
QComboBox {
    background-color: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 10px;
}
QComboBox QAbstractItemView {
    background-color: #1e293b;
    color: #e2e8f0;
    selection-background-color: #0369a1;
}
QStatusBar {
    background-color: #0c1014;
    color: #64748b;
    font-size: 11px;
}
"""

COLORES_MSG = {
    "info":    "#38bdf8",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "error":   "#ef4444",
}


class MainWindow(QMainWindow):
    """Ventana principal del simulador de arboles binarios."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Simulador de Arboles Binarios")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(ESTILO)

        # Registrar callbacks en el controlador
        self.controller.set_on_tree_changed(self._al_cambiar_arbol)
        self.controller.set_on_animation(self._al_animar)
        self.controller.set_on_message(self._al_recibir_mensaje)

        self._construir_ui()
        self._actualizar_info()

    # --------------------------------------------------
    # Construccion de la interfaz
    # --------------------------------------------------
    def _construir_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout_raiz = QHBoxLayout(central)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        # Panel izquierdo
        panel = self._construir_panel()
        panel.setFixedWidth(260)
        layout_raiz.addWidget(panel)

        # Separador visual
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color: #1e293b;")
        layout_raiz.addWidget(sep)

        # Area derecha: canvas + mensaje
        derecha = QWidget()
        layout_der = QVBoxLayout(derecha)
        layout_der.setContentsMargins(10, 10, 10, 6)
        layout_der.setSpacing(6)

        self.canvas = TreeCanvas(self.controller)
        layout_der.addWidget(self.canvas, stretch=1)

        self.lbl_mensaje = QLabel("Listo.")
        self.lbl_mensaje.setStyleSheet(f"color: {COLORES_MSG['info']}; font-size: 12px;")
        layout_der.addWidget(self.lbl_mensaje)

        layout_raiz.addWidget(derecha, stretch=1)

        # Barra de estado inferior
        self.barra = QStatusBar()
        self.setStatusBar(self.barra)
        self.lbl_info = QLabel("")
        self.lbl_info.setStyleSheet("color: #38bdf8; font-size: 12px;")
        self.barra.addPermanentWidget(self.lbl_info)

    def _construir_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet("background-color: #080b10;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(14)

        # Titulo
        titulo = QLabel("Arboles Binarios")
        titulo.setFont(QFont("Segoe UI", 15, QFont.Bold))
        titulo.setStyleSheet("color: #38bdf8; margin-bottom: 4px;")
        layout.addWidget(titulo)

        # Tipo de arbol
        grp_tipo = QGroupBox("Tipo de arbol")
        g_tipo = QVBoxLayout(grp_tipo)
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["BST", "AVL", "BT"])
        self.combo_tipo.currentTextChanged.connect(self._cambiar_tipo)
        g_tipo.addWidget(self.combo_tipo)
        layout.addWidget(grp_tipo)

        # Insertar
        grp_ins = QGroupBox("Insertar valor")
        g_ins = QVBoxLayout(grp_ins)
        self.inp_insertar = QLineEdit()
        self.inp_insertar.setPlaceholderText("Ej: 42")
        self.inp_insertar.returnPressed.connect(self._insertar)
        g_ins.addWidget(self.inp_insertar)
        btn_ins = QPushButton("Insertar")
        btn_ins.setObjectName("primario")
        btn_ins.clicked.connect(self._insertar)
        g_ins.addWidget(btn_ins)
        layout.addWidget(grp_ins)

        # Buscar
        grp_bus = QGroupBox("Buscar valor")
        g_bus = QVBoxLayout(grp_bus)
        self.inp_buscar = QLineEdit()
        self.inp_buscar.setPlaceholderText("Ej: 15")
        self.inp_buscar.returnPressed.connect(self._buscar)
        g_bus.addWidget(self.inp_buscar)
        btn_bus = QPushButton("Buscar")
        btn_bus.clicked.connect(self._buscar)
        g_bus.addWidget(btn_bus)
        layout.addWidget(grp_bus)

        # Eliminar
        grp_eli = QGroupBox("Eliminar valor")
        g_eli = QVBoxLayout(grp_eli)
        self.inp_eliminar = QLineEdit()
        self.inp_eliminar.setPlaceholderText("Ej: 10")
        self.inp_eliminar.returnPressed.connect(self._eliminar)
        g_eli.addWidget(self.inp_eliminar)
        btn_eli = QPushButton("Eliminar")
        btn_eli.setObjectName("peligro")
        btn_eli.clicked.connect(self._eliminar)
        g_eli.addWidget(btn_eli)
        layout.addWidget(grp_eli)

        # Recorridos
        grp_rec = QGroupBox("Recorridos")
        g_rec = QVBoxLayout(grp_rec)
        for nombre, etiqueta in [
            ("preorden",  "Preorden"),
            ("inorden",   "Inorden"),
            ("postorden", "Postorden"),
        ]:
            btn = QPushButton(etiqueta)
            btn.clicked.connect(lambda _, n=nombre: self.controller.recorrer(n))
            g_rec.addWidget(btn)
        layout.addWidget(grp_rec)

        # Acciones generales
        grp_acc = QGroupBox("Acciones")
        g_acc = QVBoxLayout(grp_acc)

        btn_limpiar = QPushButton("Limpiar arbol")
        btn_limpiar.setObjectName("peligro")
        btn_limpiar.clicked.connect(self._limpiar)
        g_acc.addWidget(btn_limpiar)

        btn_guardar = QPushButton("Guardar arbol")
        btn_guardar.clicked.connect(self._guardar)
        g_acc.addWidget(btn_guardar)

        btn_cargar = QPushButton("Cargar arbol")
        btn_cargar.clicked.connect(self._cargar)
        g_acc.addWidget(btn_cargar)

        layout.addWidget(grp_acc)

        layout.addStretch()

        pie = QLabel("Simulador Educativo - Estructuras de Datos")
        pie.setStyleSheet("color: #334155; font-size: 10px;")
        pie.setAlignment(Qt.AlignCenter)
        layout.addWidget(pie)

        return panel

    # --------------------------------------------------
    # Slots (respuestas a acciones del usuario)
    # --------------------------------------------------
    def _cambiar_tipo(self, tipo):
        self.controller.cambiar_tipo(tipo)

    def _insertar(self):
        self.controller.insertar(self.inp_insertar.text().strip())
        self.inp_insertar.clear()
        self.inp_insertar.setFocus()

    def _buscar(self):
        self.controller.buscar(self.inp_buscar.text().strip())
        self.inp_buscar.clear()

    def _eliminar(self):
        self.controller.eliminar(self.inp_eliminar.text().strip())
        self.inp_eliminar.clear()

    def _limpiar(self):
        self.controller.limpiar()

    def _guardar(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar arbol", "data/arbol.json", "JSON (*.json)"
        )
        if ruta:
            self.controller.guardar(ruta)

    def _cargar(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Cargar arbol", "data/", "JSON (*.json)"
        )
        if ruta:
            self.controller.cargar(ruta)
            self.combo_tipo.blockSignals(True)
            self.combo_tipo.setCurrentText(self.controller.arbol.tipo())
            self.combo_tipo.blockSignals(False)

    # --------------------------------------------------
    # Callbacks del controlador
    # --------------------------------------------------
    def _al_cambiar_arbol(self):
        self.canvas.redibujar()
        self._actualizar_info()

    def _al_animar(self, camino):
        self.canvas.animar(camino)

    def _al_recibir_mensaje(self, texto, nivel="info"):
        color = COLORES_MSG.get(nivel, COLORES_MSG["info"])
        self.lbl_mensaje.setStyleSheet(f"color: {color}; font-size: 12px;")
        self.lbl_mensaje.setText(texto)
        QTimer.singleShot(4000, lambda: self.lbl_mensaje.setText(""))

    def _actualizar_info(self):
        info = self.controller.info()
        self.lbl_info.setText(
            f"{info['tipo']}  |  Nodos: {info['nodos']}  |  "
            f"Altura: {info['altura']}  |  Raiz: {info['raiz']}"
        )