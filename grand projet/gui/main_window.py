from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer

from core.aircraft_manager import AircraftManager
from gui.radar_view import RadarView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        set.setWindowTitle("Radar ATC Simulation")
        self.setCentralWidget(QWidget())








