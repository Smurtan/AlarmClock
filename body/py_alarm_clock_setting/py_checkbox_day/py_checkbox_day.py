from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class PyCheckBoxDay(QCheckBox):
    def __init__(
            self,
            label="пн",
            parent=None
    ):
        QCheckBox.__init__(self, parent)

        self.setFixedSize(len(label) * 14, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._label = label

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRect(0, 0, self.width(), self.height())

        p.setPen(Qt.PenStyle.NoPen)

        font = p.font()
        font.setPixelSize(20)
        p.setFont(font)

        p.setBrush(QColor("#fff"))
        p.drawRoundedRect(0, 0, rect.width(), rect.height(), self.height() / 2, self.height() / 2)

        p.setPen(Qt.PenStyle.DotLine)
        p.drawText(QRect(0, -3, rect.width(), rect.height()),
                   Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self._label)

        p.end()
