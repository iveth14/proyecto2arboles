from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import (QPainter, QPen, QBrush, QColor,
                          QFont, QRadialGradient)


COLOR_FONDO        = QColor("#0f1117")
COLOR_ARISTA       = QColor("#334155")
COLOR_NODO_RELLENO = QColor("#1e293b")
COLOR_NODO_BORDE   = QColor("#38bdf8")
COLOR_TEXTO        = QColor("#f1f5f9")
COLOR_RESALTADO    = QColor("#f59e0b")   

COLOR_ENCONTRADO   = QColor("#22c55e")   
COLOR_BALANCE      = QColor("#a5f3fc")   

RADIO_NODO  = 22   
SEPARACION_Y = 70 
MARGEN_X     = 40  



class TreeCanvas(QWidget):
    

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setMinimumSize(600, 400)



     
        self._nodos_anim  = []   
        self._idx_anim    = -1    
        self._timer_anim  = QTimer(self)
        self._timer_anim.timeout.connect(self._siguiente_paso)

        self._posiciones = {}
        self._resaltados = {}



    def redibujar(self):
       
        self._calcular_posiciones()
        self.update()

    def animar(self, camino: list, intervalo_ms: int = 500):
        self._timer_anim.stop()
        self._resaltados.clear()
        self._nodos_anim = camino
        self._idx_anim   = -1
        self._timer_anim.start(intervalo_ms)


    def _calcular_posiciones(self):
        self._posiciones = {}
        raiz = self.controller.get_raiz()
        if raiz is None:
            return

        contador = [0]
        self._asignar_x_inorden(raiz, contador)

        n = self.controller.arbol.contar_nodos()
        ancho = max(self.width() - 2 * MARGEN_X, (n + 1) * (RADIO_NODO * 2 + 10))
        paso = ancho / max(n + 1, 1)

        self._asignar_coordenadas(raiz, paso, 0)

    def _asignar_x_inorden(self, nodo, contador):
        if nodo is None:
            return
        self._asignar_x_inorden(nodo.izquierdo, contador)
        nodo.x = contador[0]
        contador[0] += 1
        self._asignar_x_inorden(nodo.derecho, contador)

    def _asignar_coordenadas(self, nodo, paso, profundidad):
        if nodo is None:
            return
        px = MARGEN_X + nodo.x * paso + paso / 2
        py = 50 + profundidad * SEPARACION_Y
        self._posiciones[nodo.valor] = (px, py)
        self._asignar_coordenadas(nodo.izquierdo, paso, profundidad + 1)
        self._asignar_coordenadas(nodo.derecho,   paso, profundidad + 1)


    def _siguiente_paso(self):
        self._idx_anim += 1
        if self._idx_anim >= len(self._nodos_anim):
            self._timer_anim.stop()
            self.update()
            return

        nodo = self._nodos_anim[self._idx_anim]
        es_ultimo = (self._idx_anim == len(self._nodos_anim) - 1)
        color = COLOR_ENCONTRADO if es_ultimo else COLOR_RESALTADO
        self._resaltados[nodo.valor] = color
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), COLOR_FONDO)

        raiz = self.controller.get_raiz()
        if raiz is None:
            self._dibujar_vacio(painter)
            return

        if not self._posiciones:
            self._calcular_posiciones()

        self._dibujar_aristas(painter, raiz)
        self._dibujar_nodos(painter, raiz)

    def _dibujar_vacio(self, painter):
        painter.setPen(COLOR_ARISTA)
        painter.setFont(QFont("Segoe UI", 13))
        painter.drawText(self.rect(), Qt.AlignCenter,
                         "Arbol vacio\nInserte el primer valor")

    def _dibujar_aristas(self, painter, nodo):
        if nodo is None:
            return
        pos_p = self._posiciones.get(nodo.valor)
        if pos_p is None:
            return
        painter.setPen(QPen(COLOR_ARISTA, 2))
        for hijo in (nodo.izquierdo, nodo.derecho):
            if hijo:
                pos_h = self._posiciones.get(hijo.valor)
                if pos_h:
                    painter.drawLine(int(pos_p[0]), int(pos_p[1]),
                                     int(pos_h[0]), int(pos_h[1]))
                self._dibujar_aristas(painter, hijo)

    def _dibujar_nodos(self, painter, nodo):
        if nodo is None:
            return
        pos = self._posiciones.get(nodo.valor)
        if pos is None:
            return

        x, y = int(pos[0]), int(pos[1])
        color_res = self._resaltados.get(nodo.valor)

        grad = QRadialGradient(x - RADIO_NODO // 3, y - RADIO_NODO // 3, RADIO_NODO * 2)
        if color_res:
            grad.setColorAt(0, color_res.lighter(130))
            grad.setColorAt(1, color_res.darker(150))
            borde = color_res
        else:
            grad.setColorAt(0, QColor("#263450"))
            grad.setColorAt(1, COLOR_NODO_RELLENO)
            borde = COLOR_NODO_BORDE

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(borde, 2))
        painter.drawEllipse(x - RADIO_NODO, y - RADIO_NODO,
                            RADIO_NODO * 2, RADIO_NODO * 2)

        painter.setFont(QFont("Consolas", 10, QFont.Bold))
        painter.setPen(COLOR_TEXTO)
        painter.drawText(QRectF(x - RADIO_NODO, y - RADIO_NODO,
                                RADIO_NODO * 2, RADIO_NODO * 2),
                         Qt.AlignCenter, str(nodo.valor))

        if self.controller.arbol.tipo() == "AVL":
            fb_dict = self.controller.arbol.info_balance()
            fb = fb_dict.get(nodo.valor, 0)
            painter.setFont(QFont("Segoe UI", 7))
            painter.setPen(COLOR_BALANCE)
            

        self._dibujar_nodos(painter, nodo.izquierdo)
        self._dibujar_nodos(painter, nodo.derecho)

    def resizeEvent(self, event):
        self._calcular_posiciones()
        super().resizeEvent(event)

    def get_raiz(self):
        return self.arbol.raiz
