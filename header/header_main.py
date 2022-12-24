from PyQt6.QtCore import QTimer, QRect, QDateTime, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QFrame, QLabel

from header.close_button import PyCloseButton


class Ui_Header:
    def __init__(
            self,
            MainWindow: QMainWindow,
            parent: QWidget,
            label_font_family: str = "Segoe UI",
            label_font_point_size: int = 75
    ):
        self._MainWindow = MainWindow

        self.header = QFrame(parent)
        self.header.setGeometry(QRect(0, 0, 620, 300))
        self.header.setObjectName("header")

        self.close_button = PyCloseButton(self.header)
        self.close_button.setGeometry(160, 8, 340, 45)
        self.close_button.clicked.connect(self.minimized)

        self.font_time = QFont()
        self.font_time.setFamily(label_font_family)
        self.font_time.setPointSize(label_font_point_size)

        self.timer_update_time = QTimer()
        self.timer_update_time.setInterval(1000)  # time in millisecond
        self.timer_update_time.timeout.connect(self.updateCurrentTime)
        self.timer_update_time.start()

        self.time_label = QLabel(QDateTime.currentDateTime().toString("hh:mm"), self.header)
        self.time_label.setGeometry(QRect(190, 80, 240, 85))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setFont(self.font_time)
        self.time_label.setObjectName("time_label")

    def updateCurrentTime(self) -> None:
        self.time_label.setText(QDateTime.currentDateTime().toString("hh:mm"))

    def minimized(self) -> None:
        self._MainWindow.minimizedWindow()
