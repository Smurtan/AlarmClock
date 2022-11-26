from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class PyCloseButton(QPushButton):
    def __init__(
            self,
            parent=None,
            width=170,
            height=50,
            bg_color="",
            active_color="",
            cross_color="",
            cross_width=""
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

        rect = QRect(0, 0, self.width(), self.height())

        p.setPen(Qt.PenStyle.DashLine)

        p.setBrush(QColor(self._bg_color))
        p.drawChord(50, 100, rect.width(), rect.height(), 30 * 16, 120 * 16)

        p.setBrush(QColor(self._cross_color))
        p.drawLine(QPoint(self.width() // 2 - 20, self.height() // 2 - 10),
                   QPoint(self.width() // 2 + 20, self.height() // 2 + 10))
        p.drawLine(QPoint(self.width() // 2 + 20, self.height() // 2 - 10),
                   QPoint(self.width() // 2 - 20, self.height() // 2 + 10))

        p.end()
