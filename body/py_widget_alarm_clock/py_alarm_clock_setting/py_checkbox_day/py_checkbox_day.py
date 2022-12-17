from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class PyCheckBoxDay(QCheckBox):
    def __init__(
            self,
            label="пн",
            parent=None,
            circle_color="#fff",
            text_color="#fff",
            active_text_color="fff"
    ):
        QCheckBox.__init__(self, parent)

        self.setFixedSize(len(label) * 18 + 6, 42)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._label = label

        self._circle_color = circle_color
        self._text_color = text_color
        self._active_text_color = active_text_color

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRect(0, 0, self.width(), self.height())

        p.setPen(Qt.PenStyle.SolidLine)

        font = p.font()
        font.setPixelSize(22)
        p.setFont(font)

        if not self.isChecked():
            p.setPen(QColor(self._text_color))
            p.drawText(QRect(0, -2, rect.width(), rect.height()),
                       Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self._label)

        else:
            circle_path = QPainterPath()
            circle_path.addRoundedRect(2, 2, rect.width() - 5, rect.height() - 5, self.height() / 2, self.height() / 2)

            circle_pen = QPen()
            circle_pen.setColor(QColor(self._circle_color))
            circle_pen.setWidth(2)

            p.strokePath(circle_path, circle_pen)

            p.setPen(QColor(self._active_text_color))
            p.drawText(QRect(0, -2, rect.width(), rect.height()),
                       Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self._label)

        p.end()
