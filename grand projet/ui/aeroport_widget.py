from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt, QRectF

class AeroportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            #fond vert
            painter.setBrush(QBrush(QColor(100, 150, 100)))
            painter.drawRect(self.rect())

            #Piste grise
            piste = QRectF(250, 200, 300, 60)
            painter.setBrush(QBrush(QColor(60, 60, 60)))
            painter.drawReact(piste)

            #ligne blanche
            pen = QPen(Qt.white, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(piste.left() + 10, piste.center().y(), piste.right - 10, piste.center().y())

            #Taxiway jaune
            pen = QPen(QColor(255, 215, 0), 4)
            painter.setPen(pen)
            painter.drawline(piste.right(), piste.center().y(), 700, 300)
            painter.drawLine(700, 300, 700, 450)

            #Parking
            painter.setBrush(QBrush(QColor(180, 180, 180)))
            for i in range(4):
                painter.drawRect(QRectF(720, 330 + i * 40, 60, 30))

            #Texte
            painter.setPen(Qt.white)
            painter.drawText(piste.center().x() - 15, piste.top() - 5, "09")
            painter.drawText(piste.center().x() + 120, piste.bottom() + 15, "27")
            painter.drawText(740, 320, "Parking Avions")

            painter.end()

