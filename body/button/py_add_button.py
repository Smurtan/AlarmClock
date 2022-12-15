from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class PyAddButton(QPushButton):
    def __init__(
            self,
            parent=None,
            width=340,
            height=40,
            bg_color="#fed402"
    ):
        QPushButton.__init__(self, parent)

        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._bg_color = bg_color

    def paintEvent(self, a0: QPaintEvent) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(Qt.GlobalColor.white)
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setWidth(1)

        p.setPen(pen)

        if self.underMouse():
            p.setOpacity(1)
        else:
            p.setOpacity(0.6)

        p.setBrush(QColor(self._bg_color))
        p.drawChord(0, -100, 300, 140, -30 * 16, -120 * 16)

        font = QFont()
        font.setPixelSize(17)
        font.setFamily("Segoe UI")
        font.setBold(True)
        p.setFont(font)

        p.setPen(QPen(QPen(Qt.GlobalColor.black)))
        p.drawText(QPoint(110, 25), "Добавить")

        p.end()
