import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from controllers.tree_controller import TreeController
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Simulador de Arboles Binarios")
    app.setFont(QFont("Segoe UI", 10))

    controller = TreeController()
    ventana = MainWindow(controller)
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()