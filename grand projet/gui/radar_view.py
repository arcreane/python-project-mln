from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPainter

from core import aircraft
from core.aircraft_manager import AircraftManager
from .color import Color
from .radar_scene import RadarScene


class RadarView(QGraphicsView):
    def __init__(self, aircraft_manager = None, parent=None):
        self.aircraft_manager = aircraft_manager
        self.scene_obj = RadarScene(self.aircraft_manager)
        super().__init__(self.scene_obj, parent)

        self.setRenderHint(QPainter.Antialiasing)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 

        self.setBackgroundBrush(QBrush(Color.RADAR_BACKGROUND))

        self.setFrameStyle(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.scene():
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    def add_aircraft(self, aircraft):
        self.scene_obj.add_aircraft_to_scene(aircraft)

    def update_display(self):
        self.scene_obj.update_scene()

    def get_scene(self):
        return self.scene_obj
