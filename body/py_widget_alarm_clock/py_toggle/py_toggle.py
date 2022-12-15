from PyQt6.QtCore import (Qt, QRect, QPoint, QEasingCurve,
                          QPropertyAnimation, pyqtProperty)
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QCheckBox


class PyToggle(QCheckBox):
    def __init__(
            self,
            width=60,
            bg_color="#330ba2",
            active_color="#00BCff",
            animation_curve=QEasingCurve.Type.OutQuint
    ):
        QCheckBox.__init__(self)

        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._bg_color = bg_color
        self._activate_color = active_color

        self._emoji_position = 0
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)  # Time in milliseconds

        self.stateChanged.connect(self.start_transition)

    @pyqtProperty(int)  # Get
    def circle_position(self):
        return self._emoji_position

    @circle_position.setter
    def circle_position(self, pos):
        self._emoji_position = pos
        self.update()

    def start_transition(self, value):
        self.animation.stop()  # Stop animation if running
        if value:
            self.animation.setEndValue(self.width() - 28)
        else:
            self.animation.setEndValue(0)
        self.animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    # DRAW NEW ITEMS
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.PenStyle.NoPen)

        # CHANGING THE FONT FOR EMOTICONS
        font = p.font()
        font.setPixelSize(20)
        p.setFont(font)

        rect = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), rect.height(), self.height() / 2, self.height() / 2)

            p.setPen(Qt.PenStyle.SolidLine)
            p.drawText(QPoint(self._emoji_position, 21), "\U0001F634")  # emoticons in unicode
        else:
            p.setBrush(QColor(self._activate_color))
            p.drawRoundedRect(0, 0, rect.width(), rect.height(), self.height() / 2, self.height() / 2)

            p.setPen(Qt.PenStyle.SolidLine)
            p.drawText(QPoint(self._emoji_position, 21), "\U0001F60A")  # emoticons in unicode

        p.end()
