import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation Tour de controle")
        self.setFixedSize(1280, 720)

        self.button1 = QPushButton("button 1")
        self.button1.clicked.connect(self.boutton_clique)

        self.setCentralWidget(self.button1)

    def boutton_clique(self):
        print("clique")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()