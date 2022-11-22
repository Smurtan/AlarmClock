from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from .py_widget_alarm_clock import PyAlarmClock


class Ui_Body:
    def __init__(self, parent):
        # SET DEFAULT PARAMETERS
        self.height_alarm_clock = 100
        self.spacing_alarm_clock = 20

        # CREATING A WIDGET TO DISPLAY ALARM CLOCKS
        self.alarm_clock_area = QFrame()
        self.alarm_clock_area.setGeometry(QRect(0, 0, 620, 460))
        self.alarm_clock_area.setProperty("class", "alarm_clock_area")

        # CREAT SCROLLING WIDGET
        self.alarm_clock_scroll_area = QScrollArea(parent)
        self.alarm_clock_scroll_area.setGeometry(QRect(0, 230, 620, 340))
        self.alarm_clock_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_clock_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_clock_scroll_area.setProperty("class", "alarm_clock_scroll_area")
        self.alarm_clock_scroll_area.setWidget(self.alarm_clock_area)

        # ALIGNS ALL ALARM CLOCKS
        self.vertical_layout = QVBoxLayout(self.alarm_clock_area)
        self.vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vertical_layout.setSpacing(self.spacing_alarm_clock)

        # ALARM CLOCK STORAGE LIST
        self.list_alarm_clock = []

        # INITIALIZATION OF CREATED ALARMS
        self.list_alarm_clock = self.list_alarm_clock
        try:  # handle a small number of alarms
            self.visible_alarm_clock = self.list_alarm_clock[:3]
        except IndexError:
            self.visible_alarm_clock = self.list_alarm_clock[:len(self.list_alarm_clock)]

        # SETTING PARAMETERS FOR THE IMPLEMENTATION OF CHANGING THE SIZE OF ALARMS
        self.scroll_value = 0
        self.last_scroll = 0  # will be used to determine the scrolling direction
        self.alarm_clock_scroll_area.verticalScrollBar().valueChanged.connect(self.changingWidthAlarmClock)

    def addNewAlarmClock(self, alarm_clock_area):
        # CREAT NEW ALARM CLOCK
        new_alarm_clock = PyAlarmClock(alarm_clock_area)

        # ADDING AND EQUALIZING AN ALARM CLOCK
        # each alarm clock is aligned separately, as it has its own size
        self.vertical_layout.addWidget(new_alarm_clock, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.list_alarm_clock.append(new_alarm_clock)

        # UPDATE ALARM CLOCK SIZE
        # We will update the alarm clock sizes each time, using the scroll function to match the changes.
        self.changingWidthAlarmClock(0)

        # CHANGE SIZE OF THE ALARM CLOCK AREA
        self.alarm_clock_area.setGeometry(QRect(0, 0, 620, (len(self.list_alarm_clock) - 1) * (
                self.height_alarm_clock + self.spacing_alarm_clock) + self.height_alarm_clock))

    def changingWidthAlarmClock(self, value):

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
