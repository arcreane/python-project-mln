from PySide6.QtWidgets import QMainWindow
from ui.aeroport_widget import AeroportWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aéroport")
        self.setCentralWidget(AeroportWidget())
