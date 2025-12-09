from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer

from core.aircraft_manager import AircraftManager

from gui.radar_view import RadarView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Radar ATC Simulation")
        self.resize(1200, 800)

        self.manager = AircraftManager()

        for _ in range(6):
            self.manager.generate_random_aircraft()


        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.radar = RadarView(aircraft_manager = self.manager)
        layout.addWidget(self.radar)
        self.setCentralWidget(self.radar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(100)

    def update_simulation(self):
        self.manager.update(0.1)
        self.radar.update_display()









