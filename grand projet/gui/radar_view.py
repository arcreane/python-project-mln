from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QBrush

from gui.color import Color
from gui.radar_scene import RadarScene


class RadarView(QGraphicsView):
    def __init__(self, aircraft_manager = None, parent=None):
        self.aircraft_manager = aircraft_manager
        self.scene_obj = RadarScene(self.aircraft_manager)
        super().__init__(self.scene_obj, parent)

        self.setBackgroundBrush(QBrush(Color.RADAR_BACKGROUND))

        self.setFrameStyle(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)


    def add_aircraft(self):
        self.scene_obj.update_scene()

    def update_display(self):
        self.scene_obj.update_scene()

    def get_scene(self):
        return self.scene_obj
