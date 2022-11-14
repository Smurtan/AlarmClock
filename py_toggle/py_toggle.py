from PyQt6.QtCore import (Qt, QRect, QPoint, QEasingCurve,
                          QPropertyAnimation, pyqtProperty)
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QCheckBox, QApplication


class PyToggle(QCheckBox):
    def __init__(
            self,
            width=60,
            bg_color="#777",
            circle_color="#fefe22",
            active_color="#00BCff",
            animation_curve=QEasingCurve.Type.OutQuint
    ):
        QCheckBox.__init__(self)

        # SET DEFAULT PARAMETERS
        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._activate_color = active_color

        # CREAT ANIMATION
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)  # Time in milliseconds

        # CONNECT STATE CHANGED
        self.stateChanged.connect(self.start_transition)

    # CREAT NEW SET AND GET PROPERTY
    @pyqtProperty(int)  # Get
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transition(self, value):
        self.animation.stop()  # Stop animation if running
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)

        # START ANIMATION
        self.animation.start()

    # SET NEW HIT AREA
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    # DRAW NEW ITEMS
    def paintEvent(self, e):
        # SET PAINTER
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # SET AS ON PEN
        p.setPen(Qt.PenStyle.NoPen)

        # DRAW RECTANGLE
        rect = QRect(0, 0, self.width(), self.height())

        # DRAW SMILE
        # 😴🙂

        # CHECK IF IS CHECKED
        if not self.isChecked():
            # DRAW BG
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            # DRAW SMILE
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)

            p.setBrush(QColor("#000"))
            p.drawEllipse(7, 9, 4, 4)
            p.drawEllipse(16, 9, 4, 4)

            p.drawArc(QRect(QPoint(5, 5), QPoint(17, 15)))
        else:
            # DRAW BG
            p.setBrush(QColor(self._activate_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            # DRAW SMILE
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)

            p.setBrush(QColor("#000"))
            p.drawEllipse(7, 9, 4, 4)
            p.drawEllipse(16, 9, 4, 4)

            p.drawArc(7, 15, 20, 40, 190, 5700)

        # END DRAW
        p.end()
