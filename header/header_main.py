from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import sys

from header.close_button import PyCloseButton


class Ui_Header:
    def __init__(self, MainWindow, parent):
        self._MainWindow = MainWindow

        self.header = QFrame(parent)
        self.header.setGeometry(QRect(0, 0, 620, 300))
        self.header.setProperty("class", "header")

        self.close_button = PyCloseButton(self.header)
        self.close_button.setGeometry(160, 8, 340, 45)
        self.close_button.clicked.connect(self.close)

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
        # избавиться от css
        self.time_label.setProperty("class", "time_label")

    def updateCurrentTime(self):
        self.time_label.setText(QDateTime.currentDateTime().toString("hh:mm"))

    def close(self):
        self._MainWindow.close()
