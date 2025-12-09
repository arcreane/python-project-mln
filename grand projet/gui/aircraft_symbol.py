from PySide6.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtCore import Qt
from .color import Color

class AircraftSymbol(QGraphicsEllipseItem):
    def __init__(self, aircraft,scale_factor = 0.01):
        radius = 6
        super().__init__(-radius, -radius, radius*2, radius*2)
        self.ac = aircraft
        self.scale_factor = scale_factor

        self.setBrush(QBrush(Color.AIRCRAFT_NORMAL))
        self.setPen(QPen(Qt.black, 1))

        self.label = QGraphicsTextItem(self.ac.id, self)
        self.label.setBrush(QBrush(Color.TEXT_NORMAL))
        self.label.setPos(8, -2)

        self.update_symbol()

    def update_symbol(self):
        self.setPos(self.ac.x * self.scale_factor, -self.ac.y * self.scale_factor)
        if self.ac.in_collision:
            if hasattr(self.ac, 'in_collision'):
                self.setBrush(QBrush(Color.AIRCRAFT_COLLISION))
            else:
                self.setBrush(QBrush(Color.AIRCRAFT_NORMAL))

            self.label.setText(f"{self.ac.id}\n{self.ac.altitude} ft")


