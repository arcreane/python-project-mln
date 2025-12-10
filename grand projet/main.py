import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from core.aircraft_manager import AircraftManager


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    aircraft_manager = AircraftManager()
    window = MainWindow(aircraft_manager)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()