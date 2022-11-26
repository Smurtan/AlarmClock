from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import (QWidget, QFrame, QScrollArea,
                             QVBoxLayout, QPushButton)

from .py_widget_alarm_clock import PyAlarmClock


class Ui_Body:
    def __init__(self, parent: QWidget):
        self.height_alarm_clock = 100
        self.spacing_alarm_clock = 20

        self.alarm_clocks_area = QFrame()
        self.alarm_clocks_area.setGeometry(QRect(0, 0, 620, 340))
        self.alarm_clocks_area.setProperty("class", "alarm_clocks_area")

        self.alarm_clocks_scroll_area = QScrollArea(parent)
        self.alarm_clocks_scroll_area.setGeometry(QRect(0, 230, 620, 340))
        self.alarm_clocks_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_clocks_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_clocks_scroll_area.setProperty("class", "alarm_clocks_scroll_area")
        self.alarm_clocks_scroll_area.setWidget(self.alarm_clocks_area)

        # SO HAVE 1 ALARM CLOCK BY DEFAULT
        self.default_alarm_clock = PyAlarmClock(self.alarm_clocks_area, height_alarm_clock=self.height_alarm_clock)

        self.vertical_layout_alarm_clocks = QVBoxLayout(self.alarm_clocks_area)
        self.vertical_layout_alarm_clocks.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_alarm_clocks.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vertical_layout_alarm_clocks.setSpacing(self.spacing_alarm_clock)
        self.vertical_layout_alarm_clocks.addWidget(self.default_alarm_clock, alignment=Qt.AlignmentFlag.AlignHCenter)

        # INITIALIZATION OF CREATED ALARMS
        self.list_alarm_clocks = [self.default_alarm_clock]

        # SETTING PARAMETERS FOR THE IMPLEMENTATION OF CHANGING THE SIZE OF ALARMS
        self.scroll_value = 0
        self.last_scroll = 0  # will be used to determine the scrolling direction
        self.alarm_clocks_scroll_area.verticalScrollBar().valueChanged.connect(self.changingWidthAlarmClock)

        self.changingWidthAlarmClock(0)  # for the default alarm clock

        # полукруг =================================================================================================
        self.new_alarm_clock_button = QPushButton(parent)
        self.new_alarm_clock_button.setGeometry(285, 560, 50, 50)
        self.new_alarm_clock_button.setProperty("class", "new_alarm_clock_button")

    def addNewAlarmClock(self) -> None:
        new_alarm_clock = PyAlarmClock(self.alarm_clocks_area, height_alarm_clock=self.height_alarm_clock)

        # EACH ALARM CLOCKS IS ALIGNED SEPARATELY, AS IT HAS ITS OWN SIZE
        self.vertical_layout_alarm_clocks.addWidget(new_alarm_clock, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.list_alarm_clocks.append(new_alarm_clock)

        # AUTOMATICALLY CHANGE THE WIDTH OF ALL ALARM CLOCKS
        self.changingWidthAlarmClock(0)

        # THE WIDTH OF THE AREA ADJUSTS TO THE NUMBER OF ALARM CLOCKS
        self.alarm_clocks_area.setGeometry(QRect(0, 0, 620, (len(self.list_alarm_clocks) - 1) * (
                self.height_alarm_clock + self.spacing_alarm_clock) + self.height_alarm_clock))

    def determiningDirectionScrolling(self, scrolled_pixels: int) -> int:
        if self.last_scroll < scrolled_pixels:
            return 1  # down
        else:
            return 0  # up

    def changingWidthAlarmClock(self, scrolled_pixels: int) -> None:
        count_scroll = scrolled_pixels // 60
        first_visible_alarm_clock = scrolled_pixels // 120
        count_alarm_clocks = len(self.list_alarm_clocks)

        scroll_direction = self.determiningDirectionScrolling(scrolled_pixels)
        count_scroll -= scroll_direction * -1  # so that the size changes correctly when scrolling down

        self.last_scroll = scrolled_pixels

        # THE LIST OF VISIBLE ALARMS CHANGES ONLY WHEN 3 WHOLE ALARMS ARE VISIBLE
        if (count_scroll + 1) % 2 != 0:
            # +4 TO THE FIRST VISIBLE ALARM CLOCK HELPS TO DETERMINE WHEN 4 ALARMS ARE VISIBLE IN THE FIELD
            if count_alarm_clocks >= first_visible_alarm_clock + 4:
                self.visible_alarm_clock = self.list_alarm_clocks[first_visible_alarm_clock + scroll_direction:
                                                                  first_visible_alarm_clock + scroll_direction + 3]
            else:
                self.visible_alarm_clock = self.list_alarm_clocks[first_visible_alarm_clock:]

        # WE WILL EXCLUDE THE INTERRUPTION IF THERE IS A SMALL NUMBER OF ALARM CLOCKS
        try:
            self.visible_alarm_clock[0].setMinimumSize(590, 100)
            # 3 WHOLE ALARM CLOCKS ARE VISIBLE
            if (count_scroll + scroll_direction) % 2 == 0:
                self.visible_alarm_clock[1].setMinimumSize(540, 100)
                self.visible_alarm_clock[2].setMinimumSize(330, 100)
            else:  # INTERMEDIATE VALUES WHEN 4 ALARMS ARE VISIBLE
                self.visible_alarm_clock[1].setMinimumSize(490, 100)
                self.visible_alarm_clock[2].setMinimumSize(260, 100)
        except IndexError:
            pass
