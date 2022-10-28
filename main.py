import sys

from PyQt6.QtCore import QSize, QTimer, QRect, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFrame, QLabel,
    QVBoxLayout, QScrollArea, QHBoxLayout, QCheckBox,
    QGroupBox, QSizePolicy
)


class Ui_MainWindow:
    """The class describes the main application window"""

    def __init__(self):
        """Contains settings of the main window and widgets"""

        # external content container
        self.container = QFrame()

        self.circle_bg = QFrame(self.container)
        self.circle_bg.setGeometry(QRect(0, 0, 620, 620))
        self.circle_bg.setProperty("class", "circle_bg")

        # application header, with time and additional information
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

        # a widget that combines all alarm clocks for the competent implementation of scrolling
        self.alarm_clock_area = QFrame()
        self.alarm_clock_area.setGeometry(QRect(0, 0, 620, 460))
        self.alarm_clock_area.setProperty("class", "alarm_clock_area")

        self.alarm_scroll_area = QScrollArea(self.circle_bg)
        self.alarm_scroll_area.setGeometry(QRect(0, 230, 620, 350))
        self.alarm_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_scroll_area.setProperty("class", "alarm_scroll_area")
        self.alarm_scroll_area.setWidget(self.alarm_clock_area)


class Alarm(Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)

        # ------------------------------so far, I will create my own alarm clocks for placement-------------------------
        self.alarm = QFrame(self.alarm_clock_area)
        self.alarm.setMinimumSize(590, 100)
        self.alarm.setProperty("class", "alarm")

        self.alarm_1 = QFrame(self.alarm_clock_area)
        self.alarm_1.setMinimumSize(540, 100)
        self.alarm_1.setProperty("class", "alarm_1")

        self.alarm_2 = QFrame(self.alarm_clock_area)
        self.alarm_2.setMinimumSize(330, 100)
        self.alarm_2.setProperty("class", "alarm_2")

        self.alarm_3 = QFrame(self.alarm_clock_area)
        self.alarm_3.setMinimumSize(260, 100)
        self.alarm_3.setProperty("class", "alarm_3")

        self.alarm_4 = QFrame(self.alarm_clock_area)
        self.alarm_4.setMinimumSize(260, 100)
        self.alarm_4.setProperty("class", "alarm_3")

        self.alarm_5 = QFrame(self.alarm_clock_area)
        self.alarm_5.setMinimumSize(260, 100)
        self.alarm_5.setProperty("class", "alarm_3")
        # ----------------------------------------------------------------------------------------------------------------

        self.list_alarm = [self.alarm, self.alarm_1, self.alarm_2, self.alarm_3, self.alarm_4, self.alarm_5]
        self.visible_alarm = self.list_alarm[:3] if len(self.list_alarm) >= 3 else self.list_alarm[
                                                                                   :len(self.list_alarm)]

        # the area with the alarm time and the icon, for left alignment
        self.space_for_time = QGroupBox(self.alarm)
        self.space_for_time.setFixedSize(170, 80)
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
        self.alarm_icon.setPixmap(self.icon_moon)

        self.alarm_time = QLabel("00:00", self.space_for_time)
        self.alarm_time.setFont(self.font_alarm_time_enable)

        self.alarm_checkbox = QCheckBox(self.alarm)

        # to align the picture and time inside the alarm clock
        self.alarm_horizontal_layout = QHBoxLayout(self.space_for_time)
        self.alarm_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.alarm_horizontal_layout.addWidget(self.alarm_icon)
        self.alarm_horizontal_layout.addWidget(self.alarm_time)

        # Alignment of elements inside the alarm clock
        self.horizontal_layout = QHBoxLayout(self.alarm)
        self.horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.horizontal_layout.addWidget(self.space_for_time, alignment=Qt.AlignmentFlag.AlignLeft)
        self.horizontal_layout.addWidget(self.alarm_checkbox, alignment=Qt.AlignmentFlag.AlignRight)

        # Alignment of all alarms
        self.vertical_layout = QVBoxLayout(self.alarm_clock_area)
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vertical_layout.setSpacing(15)
        # It was decided to align each added widget individually, because they have different sizes
        self.vertical_layout.addWidget(self.alarm, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_1, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_3, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_4, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.alarm_5, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.alarm_clock_area.setGeometry(QRect(0, 0, 620, len(self.list_alarm) * 115))

        # adding an event to the scroll
        self.scroll_value = 0
        self.alarm_scroll_area.verticalScrollBar().valueChanged.connect(self.alarms_was_scrolling)

    def alarms_was_scrolling(self, value):
        # we add an error of 50px to the current scrollbar movement so that the last alarm clock
        # I also added in size, since the scrollbar value is not enough for this
        count_scroll = (value + 50) // 60  # find out the number of scrolls made
        first_alarm = (value + 50) // 120  # find out the number of the first visible alarm clock
        print(value, count_scroll, first_alarm)
        count_alarm = len(self.list_alarm)

        # so that the list with visible alarms changes only when exactly 3 alarms are visible
        # +1 was added to first_alarm, because when 4 alarm clocks are not fully visible, it is necessary,
        # so that the size has already changed, and not waiting for their full appearance
        if count_scroll % 2 != 0:
            if count_alarm >= first_alarm + 4:
                self.visible_alarm = self.list_alarm[first_alarm + 1:first_alarm + 4]
            else:
                self.visible_alarm = self.list_alarm[count_alarm - 2:]

        self.visible_alarm[0].setMinimumSize(590, 100)
        # if 4 alarm clocks are visible on the screen, then the third of them should be smaller
        if count_scroll % 2 == 0:  # only the whole 3 alarm clocks are visible
            self.visible_alarm[1].setMinimumSize(540, 100)
            self.visible_alarm[2].setMinimumSize(330, 100)
        else:  # 4 alarms are visible, because the scrollbar is not a multiple of 100
            self.visible_alarm[1].setMinimumSize(490, 100)
            self.visible_alarm[2].setMinimumSize(260, 100)



class MainWindow(QMainWindow, Alarm):
    def __init__(self):
        super(MainWindow, self).__init__()

        # setting window size
        self.setFixedSize(QSize(620, 620))

        # we install a frame with all the contents in the central widget
        self.setCentralWidget(self.container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    window.show()

    app.exec()
