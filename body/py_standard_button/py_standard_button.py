from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class PyStandardButton(QPushButton):
    def __init__(
            self,
            label="",
            parent=None,
            width=92,
            height=25,
            bg_color="#cccccc",
            text_color="#fff",
            point_size=16
    ):
        QPushButton.__init__(self, parent)

        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._label = label
        self._point_size = point_size

        self._bg_color = bg_color
        self._text_color = text_color

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRect(0, 0, self.width(), self.height())

        p.setPen(Qt.PenStyle.NoPen)

        font = p.font()
        font.setPixelSize(self._point_size)
        p.setFont(font)

        p.setBrush(QColor(self._bg_color))
        p.drawRoundedRect(0, 0, rect.width(), rect.height(), self.height() // 3, self.height() // 3)

        p.setPen(QColor(self._text_color))
        p.drawText(QRect(0, 0, rect.width(), rect.height() - 4),
                   Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, self._label)

        p.end()
