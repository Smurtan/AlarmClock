from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPaintEvent
from PyQt6.QtWidgets import QWidget, QPushButton


class PyStandardButton(QPushButton):
    def __init__(
            self,
            label: str = "",
            parent: QWidget = None,
            width: int = 92,
            height: int = 25,
            bg_color: str = "#cccccc",
            text_color: str = "#ffffff",
            point_size: int = 16
    ):
        QPushButton.__init__(self, parent)

        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._label = label
        self._point_size = point_size

        self._bg_color = bg_color
        self._text_color = text_color

    def paintEvent(self, a0: QPaintEvent) -> None:
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
