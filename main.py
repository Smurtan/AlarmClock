import sys

from PyQt6.QtCore import QSize, QTimer, QRect, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFrame, QLabel,
    QVBoxLayout, QScrollArea, QHBoxLayout, QCheckBox
)


class Ui_MainWindow:
    """The class describes the main application window"""

    def __init__(self, Window):
        """Contains settings of the main window and widgets"""

        # window size
        Window.setMinimumSize(QSize(620, 620))
        Window.setMaximumSize(QSize(620, 620))

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
        self.alarm_clock_area.setGeometry(QRect(0, 0, 620, 460))
        self.alarm_clock_area.setProperty("class", "alarm_clock_area")


class Alarm(Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self, self)

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
        self.alarm_3.setMinimumSize(260, 100)
        self.alarm_3.setMaximumSize(260, 100)
        self.alarm_3.setProperty("class", "alarm_3")
        # ----------------------------------------------------------------------------------------------------------------

        # the area with the alarm time and the icon, for left alignment
        self.space_for_time = QFrame(self.alarm)
        self.space_for_time.setProperty("class", "space_for_time")

        self.font_alarm_time_enable = QFont()
        self.font_alarm_time_enable.setFamily("Segoe UI")
        self.font_alarm_time_enable.setBold(True)
        self.font_alarm_time_enable.setPointSize(26)

        self.font_alarm_time_disable = QFont()
        self.font_alarm_time_disable.setFamily("Segoe UI")
        self.font_alarm_time_disable.setPointSize(26)

        self.icon_sun = QPixmap('image/icon_sun.png')
        self.icon_moon = QPixmap('image/icon_moon.png')
        self.alarm_icon = QLabel(self.space_for_time)
        self.alarm_icon.setMargin(10)
        self.alarm_icon.setPixmap(self.icon_moon)

        self.alarm_time = QLabel("00:00", self.space_for_time)
        self.alarm_time.setFont(self.font_alarm_time_enable)

        self.alarm_checkbox = QCheckBox(self.alarm)

        self.horizontal_layout = QHBoxLayout(self.alarm)
        self.horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.horizontal_layout.setSpacing(15)
        self.horizontal_layout.addWidget(self.space_for_time, alignment=Qt.AlignmentFlag.AlignRight)
        self.horizontal_layout.addWidget(self.alarm_checkbox, alignment=Qt.AlignmentFlag.AlignRight)

        self.vertical_layout = QVBoxLayout(self.alarm_clock_area)
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vertical_layout.setSpacing(15)
        # It was decided to align each added widget individually, because they have different sizes
        self.vertical_layout.addWidget(self.alarm, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_1, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_3, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.alarm_scroll_area = QScrollArea(self.circle_bg)
        self.alarm_scroll_area.setGeometry(QRect(0, 230, 620, 350))
        self.alarm_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_scroll_area.setProperty("class", "alarm_scroll_area")
        self.alarm_scroll_area.setWidget(self.alarm_clock_area)


class MainWindow(QMainWindow, Alarm):
    def __init__(self):
        super(MainWindow, self).__init__()

        Alarm.__init__(self)

        self.setCentralWidget(Ui_MainWindow.container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    window.show()

    app.exec()
