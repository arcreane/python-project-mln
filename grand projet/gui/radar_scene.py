from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt
import random


from gui.aircraft_symbol import AircraftSymbol


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
        pen_grid.setStyle(Qt.PenStyle.DashLine)

        for nm in [5, 10, 20, 40, 60, 80]:
            r = nm * 6076 * self.scale_factor
            self.addEllipse(-r, -r, 2*r, 2*r, pen_grid)
        size = self.map_size * self.scale_factor/2
        self.addLine(-size, 0, size, 0, pen_grid)
        self.addLine(0, -size, 0, size, pen_grid)

    def update_scene(self):
        rect = self.sceneRect()
        for ac in self.aircraft_manager.get_all_aircrafts():
            if ac.aircraft_id not in self.aircraft_symbols:
                symbol = AircraftSymbol(ac, self.scale_factor)
                side = random.choice(['top', 'bottom', 'left', 'right'])

                x = 0
                y = 0

                match side:
                    case 'top':
                        x = random.uniform(rect.left(), rect.right())
                        y = rect.top()
                    case 'bottom':
                        x = random.uniform(rect.left(), rect.right())
                        y = rect.bottom()
                    case 'left':
                        x = rect.left()
                        y = random.uniform(rect.top(), rect.bottom())
                    case 'right':
                        x = rect.right()
                        y = random.uniform(rect.top(), rect.bottom())

                symbol.setPos(x, y)
                self.aircraft_symbols[ac.aircraft_id] = symbol
                self.addItem(symbol)
            else:
                self.aircraft_symbols[ac.aircraft_id].update_symbol()



