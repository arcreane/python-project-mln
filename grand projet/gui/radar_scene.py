from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt

from core.aircraft import Aircraft
from .aircraft_symbol import AircraftSymbol


class  RadarScene(QGraphicsScene):
    def __init__(self, aircraft_manager, map_size = 15000):
        super().__init__()

        self.aircraft_manager = aircraft_manager
        self.map_size = map_size

        self.scale_factor = 0.01   # 15000 ft > 150 px

        size_px = map_size * self.scale_factor
        self.setSceneRect(-size_px/2, -size_px/2, size_px, size_px)

        self.aircraft_symbols = {}

        self._draw_grid()

    def _draw_grid(self):
        pen_grid = QPen(QColor(80, 80, 80))
        pen_grid.setStyle(Qt.DashLine)

        for nm in [5, 10, 20, 40, 60, 80]:
            r = nm * 6076 * self.scale_factor
            self.addLine(-1000, 0, 1000, 0, pen_grid)
            self.addLine(0, -1000, 0, 1000, pen_grid)

    def update_scene(self):
        for ac in self.aircraft_manager.get_all_aircrafts():
            if ac.id not in self.aircraft_symbols:
                self.aircraft_symbols[ac.id] = AircraftSymbol(ac, self.scale_factor)
                self.addItem(self.aircraft_symbols[ac.id])

            self.aircraft_symbols[ac.id].update_symbol()

