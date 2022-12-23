from PyQt6.QtGui import QPainter, QPen, QPaintEvent, QColor, QFont
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QPushButton


class PyCloseButton(QPushButton):
    def __init__(
            self,
            parent: QWidget = None,
            width: int = 340,
            height: int = 40,
            bg_color: str = "#bb2323",
            active_color: str = "#225D44",
            stroke_color: str = "#ffffff"
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
