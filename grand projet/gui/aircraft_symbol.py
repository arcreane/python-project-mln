from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen, QFont


class AircraftSymbol(QGraphicsEllipseItem):
    """Symbole graphique d'un avion"""

    def __init__(self, aircraft):
        super().__init__(-10, -10, 20, 20)
        self.aircraft = aircraft

        # Couleurs
        self.colors = {
            "normal": QColor(0, 255, 0),  # Vert
            "collision": QColor(255, 0, 0),  # Rouge
            "warning": QColor(148, 0, 211),  # Orange - NOUVEAU pour alertes
            "emergency": QColor(255, 140, 0),  # Orange foncé
            "holding": QColor(255, 255, 0),  # Jaune
            "selected": QColor(0, 255, 255)  # Cyan
        }

        self.setPen(QPen(Qt.black, 2))
        self.setBrush(QBrush(self.colors["normal"]))

        # Label
        self.label = QGraphicsTextItem(aircraft.identifier, self)
        font = QFont("Arial", 7, QFont.Bold)
        self.label.setFont(font)
        self.label.setDefaultTextColor(self.colors["normal"])
        self.label.setPos(15, -10)

        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

    def update_color(self, state="normal"):
        """Met à jour la couleur selon l'état"""
        color = self.colors.get(state, self.colors["normal"])
        self.setBrush(QBrush(color))
        self.label.setDefaultTextColor(color)

    def mousePressEvent(self, event):
        """Gestion du clic"""
        if event.button() == Qt.LeftButton:
            self.setSelected(True)
            # Émettre un signal personnalisé
            if hasattr(self.scene(), 'aircraft_selected'):
                self.scene().aircraft_selected.emit(self)
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        """Survol de la souris"""
        self.setPen(QPen(Qt.white, 3))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Fin du survol"""
        self.setPen(QPen(Qt.black, 2))
        super().hoverLeaveEvent(event)