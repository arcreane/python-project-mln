from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPainter
from PySide6.QtGui import QWheelEvent

from gui.radar_scene import SCENE_WIDTH, SCENE_HEIGHT, BG_COLOR


class RadarView(QGraphicsView):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)
        self.setRenderHint()
        self.setVerticalScrollBarPolicy()
        self.setHorizontalScrollBarPolicy()
        self.setBackgroundBrush((QBrush(BG_COLOR)))

    def wheelEvent(self, event : QWheelEvent):
        zoom_in = 1.15
        zoom_out = 1 / zoom_in

        if event.angleDelta().y() > 0:
            self.scale(zoom_out, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)
