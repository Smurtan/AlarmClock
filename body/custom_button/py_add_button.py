from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QPaintEvent, QFont, QColor
from PyQt6.QtWidgets import QWidget, QPushButton


class PyAddButton(QPushButton):
    def __init__(
            self,
            parent: QWidget = None,
            width: int = 340,
            height: int = 40,
            bg_color: str = "#fed402"
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
