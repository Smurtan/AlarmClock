from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class PyAddButton(QPushButton):
    def __init__(
            self,
            parent=None,
            width=302,
            height=40,
            bg_color="#29b078",
            active_color="225D44FF",
            plus_color="B02929FF",
            plus_width=30
    ):
        QPushButton.__init__(self, parent)

        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._bg_color = bg_color
        self._active_color = active_color
        self._plus_color = plus_color

        self._plus_width = plus_width

    def paintEvent(self, a0: QPaintEvent) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.PenStyle.NoPen)

        p.setBrush(QColor(self._bg_color))
        p.drawChord(-160, -580, 620, 620, -58 * 16, -64 * 16)

        p.setPen(Qt.PenStyle.SolidLine)

        pen = QPen()
        pen.setWidth(3)
        p.setPen(pen)
        p.setBrush(QColor(self._plus_color))
        p.drawLine(QPoint(self.width() // 2 - self._plus_width // 2, 20),
                   QPoint(self.width() // 2 + self._plus_width // 2, 20))
        p.drawLine(QPoint(self.width() // 2, 20 - self._plus_width // 2),
                   QPoint(self.width() // 2, 20 + self._plus_width // 2))

        p.end()
