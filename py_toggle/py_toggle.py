from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QCheckBox


class PyToggle(QCheckBox):
    def __init__(
            self,
            width=60,
            bg_color="#777",
            circle_color="#DDD",
            active_color="#00BCff"
    ):
        QCheckBox.__init__(self)

        # SET DEFAULT PARAMETERS
        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._activate_color = active_color

    def paintEvent(self, e):
        # SET PAINTER
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # SET AS ON PEN
        p.setPen(Qt.PenStyle.NoPen)

        # DRAW RECTANGLE
        rect = QRect(0, 0, self.width(), self.height())

        # DRAW BG
        p.setBrush(QColor(self._bg_color))
        p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

        # END DRAW
        p.end()
