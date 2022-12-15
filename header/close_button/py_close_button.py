from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class PyCloseButton(QPushButton):
    def __init__(
            self,
            parent=None,
            width=340,
            height=40,
            bg_color="#bb2323",
            active_color="225D44FF",
            stroke_color="FFFFFF"
    ):
        QPushButton.__init__(self, parent)

        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._bg_color = bg_color
        self._active_color = active_color
        self._stroke_color = stroke_color

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
            p.setOpacity(0.3)

        p.setBrush(QColor(self._bg_color))
        p.drawChord(0, 2, 300, 140, 30 * 16, 120 * 16)

        font = QFont()
        font.setPixelSize(17)
        font.setFamily("Segoe UI")
        font.setBold(True)
        p.setFont(font)

        p.drawText(QPoint(116, 25), "Закрыть")

        p.end()
