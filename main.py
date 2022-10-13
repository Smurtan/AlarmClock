import sys

from PyQt6.QtCore import QSize, QTimer, QRect, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFrame, QLabel,
    QGroupBox, QVBoxLayout
)


class MainWindow(QMainWindow):
    """The class describes the main application window"""

    def __init__(self):
        """Contains settings of the main window and widgets"""

        super(MainWindow, self).__init__()

        # window size
        self.setMinimumSize(QSize(620, 620))
        self.setMaximumSize(QSize(620, 620))

        # external content container
        self.container = QFrame()

        self.circle_bg = QFrame(self.container)
        self.circle_bg.setMinimumSize(QSize(620, 620))
        self.circle_bg.setMaximumSize(QSize(620, 620))
        self.circle_bg.setProperty("class", "circle_bg")

        self.header = QFrame(self.circle_bg)
        self.header.setGeometry(QRect(0, 0, 620, 230))
        self.header.setProperty("class", "header")

        self.font_time = QFont()
        self.font_time.setFamily("Segoe UI")
        self.font_time.setPointSize(75)

        self.time_label = QLabel("00:00", self.header)
        self.time_label.setGeometry(QRect(0, 0, 620, 230))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.time_label.setFont(self.font_time)
        self.time_label.setProperty("class", "time_label")

        self.alarm_clock_area = QFrame(self.circle_bg)
        self.alarm_clock_area.setGeometry(QRect(0, 230, 620, 390))
        self.alarm_clock_area.setProperty("class", "alarm_clock_area")

        self.alarm = QFrame(self.alarm_clock_area)
        self.alarm.setMinimumSize(500, 90)
        self.alarm.setMaximumSize(500, 90)
        self.alarm.setProperty("class", "alarm")

        self.alarm_1 = QFrame(self.alarm_clock_area)
        self.alarm_1.setMinimumSize(300, 90)
        self.alarm_1.setMaximumSize(300, 90)
        self.alarm_1.setProperty("class", "alarm")

        self.verticalLayout = QVBoxLayout(self.alarm_clock_area)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.addWidget(self.alarm, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.alarm_1, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setCentralWidget(self.container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    window.show()

    app.exec()
