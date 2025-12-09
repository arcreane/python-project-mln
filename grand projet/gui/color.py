from PySide6.QtGui import QColor

class Color:
    RADAR_BACKGROUND = QColor(10, 30, 30)
    RADAR_GRID = QColor(80, 120, 120)
    RADAR_CIRCLE = QColor(120, 160, 160)
    RADAR_AZIMUTH = QColor(0, 200, 200)

    AIRCRAFT_NORMAL = QColor(0, 255, 255)
    AIRCRAFT_SELECTED = QColor(255, 255, 0)
    AIRCRAFT_COLLISION = QColor(255, 0, 0)

    AIRCRAFT_HEADING = QColor(255, 255, 0)

    TEXT_NORMAL = QColor(0, 255, 255)
    TEXT_SELECTED = QColor(255, 255, 0)
    TEXT_WARNING = QColor(255, 80, 0)

    AIRPORT_ZONE = QColor(255, 165, 0)