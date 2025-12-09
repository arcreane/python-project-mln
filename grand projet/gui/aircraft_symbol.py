from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtGui import QColor, QPen, QBrush
from gui.color import Color

class AircraftSymbol(QGraphicsEllipseItem):
    def __init__(self, aircraft,scale_factor = 0.01):
        radius = 6
        super().__init__(-radius, -radius, radius*2, radius*2)
        self.aircraft = aircraft
        self.scale_factor = scale_factor

        self.setBrush(QBrush(Color.AIRCRAFT_NORMAL))
        self.setPen(QPen(Color.TEXT_NORMAL, 1))

        self.label = QGraphicsTextItem(self.aircraft.aircraft_id, self)
        self.label.setDefaultTextColor(Color.TEXT_NORMAL)
        self.label.setPos(8, -2)

        self.update_symbol()

    def update_symbol(self):
        self.setPos(self.aircraft.x * self.scale_factor, -self.aircraft.y * self.scale_factor)
        if self.aircraft.in_collision:
            self.setBrush(QBrush(Color.AIRCRAFT_COLLISION))
        else:
            self.setBrush(QBrush(Color.AIRCRAFT_NORMAL))

        self.label.setPlainText(f"{self.aircraft.id}\n{self.aircraft.altitude} ft")


