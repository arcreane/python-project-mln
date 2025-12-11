from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, Property, Signal
from PySide6.QtGui import QColor, QBrush, QPen, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsObject, \
    QGraphicsLineItem, QGraphicsRectItem
from .aircraft_symbol import AircraftSymbol
import math

BG_COLOR = QColor(10, 30, 30)


class RotatingLine(QGraphicsObject):

    def __init__(self, length, pen, parent=None):
        super().__init__(parent)
        self._rotation = 0
        self.length = length
        self.pen = pen

    def getRotation(self):
        return self._rotation

    def setRotation(self, value):
        self._rotation = value
        self.update()

    rotation = Property(float, getRotation, setRotation)

    def boundingRect(self):
        return QRectF(-self.length, -self.length, 2 * self.length, 2 * self.length)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)
        painter.save()
        painter.rotate(self._rotation)
        painter.drawLine(0, 0, 0, -self.length)
        painter.restore()


class RadarScene(QGraphicsScene):
    aircraft_selected = Signal(object)

    def __init__(self, parent=None, radar_radius=500):
        super().__init__(parent)
        self.radius = radar_radius
        self.aircraft_symbols = {}
        self.route_lines = []

        scene_size = radar_radius * 2

        self.setSceneRect(-scene_size, -scene_size, scene_size * 2, scene_size * 2)
        self.setBackgroundBrush(QBrush(BG_COLOR))

        self._build_grid()
        self._build_runway()
        self._build_scanline()

    def _build_grid(self):
        r = self.radius

        circle = QGraphicsEllipseItem(-r, -r, 2 * r, 2 * r)
        circle.setPen(QPen(QColor(0, 255, 0), 2))
        self.addItem(circle)

        for k in [0.25, 0.5, 0.75]:
            cr = r * k
            c = QGraphicsEllipseItem(-cr, -cr, 2 * cr, 2 * cr)
            c.setPen(QPen(QColor(0, 120, 120), 1, Qt.DotLine))
            self.addItem(c)

        pen = QPen(QColor(0, 120, 120), 1)
        self.addLine(-r, 0, r, 0, pen)
        self.addLine(0, -r, 0, r, pen)


        font = QFont("Arial", 12, QFont.Bold)
        for angle in range(0, 360, 30):
            a = math.radians(angle - 90)
            x = r * math.cos(a)
            y = r * math.sin(a)


            line = QGraphicsLineItem((r - 15) * math.cos(a), (r - 15) * math.sin(a),r * math.cos(a), r * math.sin(a))

            line.setPen(QPen(QColor(0, 255, 0), 2))
            self.addItem(line)


            text_offset = 25
            x_text = (r + text_offset) * math.cos(a)
            y_text = (r + text_offset) * math.sin(a)

            t = QGraphicsTextItem(str(angle if angle != 0 else "360/0"))
            t.setFont(font)
            t.setDefaultTextColor(QColor(0, 255, 0))
            t.setPos(x_text - 15, y_text - 10)
            self.addItem(t)

    def _build_runway(self):
        runway_width = 40
        runway_length = 100

        runway = QGraphicsRectItem(-runway_width / 2, -runway_length / 2,
                                   runway_width, runway_length)
        runway.setPen(QPen(QColor(255, 255, 0), 2))
        runway.setBrush(QBrush(QColor(80, 80, 80)))
        self.addItem(runway)

        for i in range(-3, 4):
            line = QGraphicsLineItem(-runway_width / 4, i * 15, runway_width / 4, i * 15)
            line.setPen(QPen(QColor(255, 255, 255), 1))
            self.addItem(line)

        label = QGraphicsTextItem("RWY")
        label.setFont(QFont("Arial", 10, QFont.Bold))
        label.setDefaultTextColor(QColor(255, 255, 0))
        label.setPos(-15, runway_length / 2 + 5)
        self.addItem(label)

    def _build_scanline(self):
        pen = QPen(QColor(0, 255, 0, 120), 2)
        self.scanline = RotatingLine(length=self.radius, pen=pen)
        self.scanline.setPos(0, 0)
        self.addItem(self.scanline)

        anim = QPropertyAnimation(self.scanline, b"rotation")
        anim.setStartValue(0)
        anim.setEndValue(360)
        anim.setDuration(4000)
        anim.setLoopCount(-1)
        anim.start()
        self.scan_anim = anim

    def draw_routes(self, route_manager):
        for line in self.route_lines:
            self.removeItem(line)
        self.route_lines = []

        scale = self.radius / 100000

        for route_name, route in route_manager.routes.items():
            if route.route_type == "cruise":
                color = QColor(100, 100, 255, 80)
            else:
                color = QColor(255, 165, 0, 80)

            pen = QPen(color, 1, Qt.DashLine)

            for i in range(len(route.waypoints) - 1):
                wp1 = route.waypoints[i]
                wp2 = route.waypoints[i + 1]

                x1 = wp1.x * scale
                y1 = wp1.y * scale
                x2 = wp2.x * scale
                y2 = wp2.y * scale

                line = QGraphicsLineItem(x1, y1, x2, y2)
                line.setPen(pen)
                self.addItem(line)
                self.route_lines.append(line)

    def add_aircraft_to_scene(self, aircraft):
        symbol = AircraftSymbol(aircraft)
        self.addItem(symbol)
        self.aircraft_symbols[aircraft.identifier] = symbol

    def update_positions(self):
        scale = self.radius / 100000

        for ac_id, sym in list(self.aircraft_symbols.items()):
            ac = sym.aircraft

            is_destroyed = getattr(ac, 'is_destroyed', False)


            if ac.has_landed or is_destroyed:
                self.removeItem(sym)
                if sym in self.items():
                    self.removeItem(sym)
                del self.aircraft_symbols[ac_id]
                continue

            sym.setPos(ac.x * scale, ac.y * scale)

            sym.setPos(ac.x * scale, ac.y * scale)


            if ac.in_collision:
                sym.update_color("collision")
            elif ac.has_emergency:
                sym.update_color("emergency")
            elif ac.in_warning:
                sym.update_color("warning")
            elif ac.is_holding:
                sym.update_color("holding")
            elif sym.isSelected():
                sym.update_color("selected")
            else:
                sym.update_color("normal")



    def _on_symbol_clicked(self, symbol):
        for sym in self.aircraft_symbols.values():
            if sym != symbol:
                sym.setSelected(False)

        self.aircraft_selected.emit(symbol)