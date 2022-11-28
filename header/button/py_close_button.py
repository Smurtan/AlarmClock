from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class PyCloseButton(QPushButton):
    def __init__(
            self,
            parent=None,
            width=340,
            height=45,
            bg_color="#29b078",
            active_color="225D44FF",
            cross_color="B02929FF",
            cross_width=50
    ):
        QPushButton.__init__(self, parent)

        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._bg_color = bg_color
        self._active_color = active_color
        self._cross_color = cross_color

        self._cross_width = cross_width

    def paintEvent(self, a0: QPaintEvent) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.PenStyle.NoPen)

        p.setBrush(QColor(self._bg_color))
        p.drawChord(-137, 0, 620, 620, 58 * 16, 64 * 16)

        p.setPen(Qt.PenStyle.SolidLine)

        pen = QPen()
        pen.setWidth(3)
        p.setPen(pen)
        p.setBrush(QColor(self._cross_color))
        p.drawLine(QPoint(self.width() // 2 - self._cross_width // 2, 5),
                   QPoint(self.width() // 2 + self._cross_width // 2, 35))
        p.drawLine(QPoint(self.width() // 2 + self._cross_width // 2, 5),
                   QPoint(self.width() // 2 - self._cross_width // 2, 35))

        p.end()
