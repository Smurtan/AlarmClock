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

        self.alarm_clock_scroll_area = QScrollArea(self.circle_bg)
        self.alarm_clock_scroll_area.setGeometry(QRect(0, 230, 620, 340))
        self.alarm_clock_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_clock_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_clock_scroll_area.setProperty("class", "alarm_clock_scroll_area")
        self.alarm_clock_scroll_area.setWidget(self.alarm_clock_area)


class AlarmClock(Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)

        self.width_alarm_clock = 100
        self.spacing_alarm_clock = 20

        self.list_alarm_clock = []

        if len(self.list_alarm_clock) >= 3:
            self.visible_alarm_clock = self.list_alarm_clock[:3]
        else:
            self.visible_alarm_clock = self.list_alarm_clock[:len(self.list_alarm_clock)]

        self.font_alarm_clock_time_enable = QFont()
        self.font_alarm_clock_time_enable.setFamily("Segoe UI")
        self.font_alarm_clock_time_enable.setBold(True)
        self.font_alarm_clock_time_enable.setPointSize(26)

        self.font_alarm_clock_time_disable = QFont()
        self.font_alarm_clock_time_disable.setFamily("Segoe UI")
        self.font_alarm_clock_time_disable.setPointSize(26)

        self.icon_sun = QPixmap('image/icon_sun.png')
        self.icon_moon = QPixmap('image/icon_moon.png')

        # Alignment of all alarm clocks
        self.vertical_layout = QVBoxLayout(self.alarm_clock_area)
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vertical_layout.setSpacing(self.spacing_alarm_clock)

        # adding an event to the scroll
        self.scroll_value = 0
        self.last_scroll = 0  # will be used to determine the scrolling direction
        self.alarm_clock_scroll_area.verticalScrollBar().valueChanged.connect(self.alarm_clocks_was_scrolling)

    def AddingNewAlarmClock(self, time):
        alarm_clock = QFrame(self.alarm_clock_area)
        alarm_clock.setMinimumSize(260, 100)
        alarm_clock.setProperty("class", "alarm_clock")

        # the area with the alarm time and the icon, for left alignment
        space_for_time = QGroupBox(alarm_clock)
        space_for_time.setFixedSize(170, 80)
        space_for_time.setProperty("class", "space_for_time")

        alarm_clock_icon = QLabel(space_for_time)
        alarm_clock_icon.setPixmap(self.icon_moon)

        alarm_clock_time = QLabel(time, space_for_time)
        alarm_clock_time.setFont(self.font_alarm_clock_time_enable)

        alarm_clock_checkbox = QCheckBox(alarm_clock)

        # to align the picture and time inside the space for time
        space_for_time_horizontal_layout = QHBoxLayout(space_for_time)
        space_for_time_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        space_for_time_horizontal_layout.addWidget(alarm_clock_icon)
        space_for_time_horizontal_layout.addWidget(alarm_clock_time)

        # Alignment of elements inside the alarm clock
        alarm_clock_horizontal_layout = QHBoxLayout(alarm_clock)
        alarm_clock_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        alarm_clock_horizontal_layout.addWidget(space_for_time, alignment=Qt.AlignmentFlag.AlignLeft)
        alarm_clock_horizontal_layout.addWidget(alarm_clock_checkbox, alignment=Qt.AlignmentFlag.AlignRight)

        # It was decided to align each added widget individually, because they have different sizes
        self.vertical_layout.addWidget(alarm_clock, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.list_alarm_clock.append(alarm_clock)

        # We will update the alarm clock sizes each time, using the scroll function to match the changes.
        self.alarm_clocks_was_scrolling(0)

        # we change the size of the alarm clock area so that everyone fits in
        self.alarm_clock_area.setGeometry(QRect(0, 0, 620, (len(self.list_alarm_clock) - 1) * (
                self.width_alarm_clock + self.spacing_alarm_clock) + self.width_alarm_clock))

    def alarm_clocks_was_scrolling(self, value):
        count_scroll = value // 60  # find out the number of scrolls made
        first_alarm_clock = value // 120  # find out the number of the first visible alarm clock
        count_alarm_clock = len(self.list_alarm_clock)

        # determining the direction of scrolling
        # it is necessary that the program correctly determines which alarm clock is currently visible
        if self.last_scroll < value:
            scroll_direction = 1
            count_scroll -= 1  # чтобы при прокрутке вниз правильно менялся размер
        else:
            scroll_direction = 0

        self.last_scroll = value  # updating the old position

        # so that the list with visible alarm clocks changes only when exactly 3 alarm clocks are visible
        # +1 was added to first_alarm, because when 4 alarm clocks are not fully visible, it is necessary,
        # so that the size has already changed, and not waiting for their full appearance
        if (count_scroll + 1) % 2 != 0:
            if count_alarm_clock >= first_alarm_clock + 4:
                self.visible_alarm_clock = self.list_alarm_clock[first_alarm_clock + scroll_direction:
                                                                 first_alarm_clock + scroll_direction + 3]
            else:
                self.visible_alarm_clock = self.list_alarm_clock[count_alarm_clock - 3:]

        # We will exclude the interruption if there is a small number of alarms
        try:
            self.visible_alarm_clock[0].setMinimumSize(590, 100)
            # if 4 alarm clocks are visible on the screen, then the third of them should be smaller
            if (count_scroll + scroll_direction) % 2 == 0:  # only the whole 3 alarm clocks are visible
                self.visible_alarm_clock[1].setMinimumSize(540, 100)
                self.visible_alarm_clock[2].setMinimumSize(330, 100)
            else:  # 4 alarm clocks are visible, because the scrollbar is not a multiple of 100
                self.visible_alarm_clock[1].setMinimumSize(490, 100)
                self.visible_alarm_clock[2].setMinimumSize(260, 100)
        except IndexError:
            pass


class MainWindow(QMainWindow, AlarmClock):
    def __init__(self):
        super(MainWindow, self).__init__()

        # setting window size
        self.setFixedSize(QSize(620, 620))

        AlarmClock.AddingNewAlarmClock(self, "7:00")
        AlarmClock.AddingNewAlarmClock(self, "21:00")
        AlarmClock.AddingNewAlarmClock(self, "18:00")
        AlarmClock.AddingNewAlarmClock(self, "17:00")

        # we install a frame with all the contents in the central widget
        self.setCentralWidget(self.container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    window.show()

    app.exec()
