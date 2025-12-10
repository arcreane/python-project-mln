from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPainter, QWheelEvent


class RadarView(QGraphicsView):
    """Vue du radar avec zoom"""

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        from .radar_scene import BG_COLOR
        self.setBackgroundBrush(QBrush(BG_COLOR))

        self.setDragMode(QGraphicsView.NoDrag)

    def wheelEvent(self, event: QWheelEvent):
        """Gestion du zoom avec la molette"""
        zoom_in = 1.15
        zoom_out = 1 / zoom_in

        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)