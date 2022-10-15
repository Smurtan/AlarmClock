import sys

from PyQt6.QtCore import QSize, QTimer, QRect, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFrame, QLabel,
    QVBoxLayout, QScrollArea, QScroller, QScrollBar
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
        self.circle_bg.setGeometry(QRect(0, 0, 620, 620))
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
        self.alarm_clock_area.setProperty("class", "alarm_clock_area")

# ------------------------------so far, I will create my own alarm clocks for placement-------------------------
        self.alarm = QFrame(self.alarm_clock_area)
        self.alarm.setMinimumSize(590, 100)
        self.alarm.setMaximumSize(590, 100)
        self.alarm.setProperty("class", "alarm")

        self.alarm_1 = QFrame(self.alarm_clock_area)
        self.alarm_1.setMinimumSize(530, 100)
        self.alarm_1.setMaximumSize(530, 100)
        self.alarm_1.setProperty("class", "alarm_1")

        self.alarm_2 = QFrame(self.alarm_clock_area)
        self.alarm_2.setMinimumSize(370, 100)
        self.alarm_2.setMaximumSize(370, 100)
        self.alarm_2.setProperty("class", "alarm_2")

        self.alarm_3 = QFrame(self.alarm_clock_area)
        self.alarm_3.setMinimumSize(370, 100)
        self.alarm_3.setMaximumSize(370, 100)
        self.alarm_3.setProperty("class", "alarm_3")
# ----------------------------------------------------------------------------------------------------------------

        self.vertical_layout = QVBoxLayout(self.alarm_clock_area)
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vertical_layout.setSpacing(15)
        # It was decided to align each added widget individually, because they have different sizes
        self.vertical_layout.addWidget(self.alarm, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_1, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_3, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.alarm_scroll_area = QScrollArea(self.circle_bg)
        self.alarm_scroll_area.setGeometry(QRect(0, 230, 620, 390))
        self.alarm_scroll_area.setProperty("class", "alarm_scroll_area")
        self.alarm_scroll_area.setWidget(self.alarm_clock_area)

        self.setCentralWidget(self.container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    window.show()

    app.exec()
