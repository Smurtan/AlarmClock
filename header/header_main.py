from PyQt6.QtCore import *
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *

import time

from header.button import PyCloseButton


class Ui_Header:
    def __init__(self, parent):
        self.header = QFrame(parent)
        self.header.setGeometry(QRect(0, 0, 620, 230))
        self.header.setProperty("class", "header")

        self.close_button = PyCloseButton(self.header)
        self.close_button.setGeometry(137, 0, 340, 45)

        self.font_time = QFont()
        self.font_time.setFamily("Segoe UI")
        self.font_time.setPointSize(75)

        self.timer_update_time = QTimer()
        self.timer_update_time.setInterval(1000)  # time in millisecond
        self.timer_update_time.timeout.connect(self.updateCurrentTime)
        self.timer_update_time.start()

        self.time_label = QLabel(QDateTime.currentDateTime().toString("hh:mm"), self.header)
        self.time_label.setGeometry(QRect(190, 80, 240, 85))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setFont(self.font_time)
        self.time_label.setProperty("class", "time_label")

    def updateCurrentTime(self):
        self.time_label.setText(QDateTime.currentDateTime().toString("hh:mm"))
