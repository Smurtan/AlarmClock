from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from py_toggle import PyToggle


class PyAlarmClock(QWidget):
    def __init__(
            self,
            family_fonts="Segoe UI",
            point_size=26,
            icon_day="icon_sun.png",
            icon_night="icon_moon.png",
            minheight_alarm_clock=100,
            minwidth_alarm_clock=290,
            list_alarm_clock=list,
            parent=None
    ):
        QWidget.__init__(self)

        # SET DEFAULT FONTS
        self.font_alarm_clock_time_enable = QFont()
        self.font_alarm_clock_time_enable.setFamily(family_fonts)
        self.font_alarm_clock_time_enable.setBold(True)
        self.font_alarm_clock_time_enable.setPointSize(point_size)

        self.font_alarm_clock_time_disable = QFont()
        self.font_alarm_clock_time_disable.setFamily(family_fonts)
        self.font_alarm_clock_time_disable.setPointSize(point_size)

        # SET ICON
        self.icon_day = QPixmap('image/' + icon_day)
        self.icon_night = QPixmap('image/' + icon_night)

        # INITIALIZATION OF CREATED ALARMS
        self.list_alarm_clock = list_alarm_clock
        try:  # handle a small number of alarms
            self.visible_alarm_clock = self.list_alarm_clock[:3]
        except IndexError:
            self.visible_alarm_clock = self.list_alarm_clock[:len(self.list_alarm_clock)]

        # CREATE NEW ALARM CLOCK
        self.alarm_clock = QFrame(parent)
        self.alarm_clock.setMinimumSize(minwidth_alarm_clock, minheight_alarm_clock)
        self.alarm_clock.setProperty("class", "alarm_clock")



        # adding an event to the scroll
        self.scroll_value = 0
        self.last_scroll = 0  # will be used to determine the scrolling direction
        self.alarm_clock_scroll_area.verticalScrollBar().valueChanged.connect(self.alarm_clocks_was_scrolling)

        # CREAT ANIMATION
        self._alarm_clock_width = 590
        self.animation = QPropertyAnimation(self, )

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

        # animated toggle button===========================================================================
        alarm_clock_toggle = PyToggle()
        # ==================================================================================================

        # to align the picture and time inside the space for time
        space_for_time_horizontal_layout = QHBoxLayout(space_for_time)
        space_for_time_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        space_for_time_horizontal_layout.addWidget(alarm_clock_icon)
        space_for_time_horizontal_layout.addWidget(alarm_clock_time)

        # Alignment of elements inside the alarm clock
        alarm_clock_horizontal_layout = QHBoxLayout(alarm_clock)
        alarm_clock_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        alarm_clock_horizontal_layout.addWidget(space_for_time, alignment=Qt.AlignmentFlag.AlignLeft)
        alarm_clock_horizontal_layout.addWidget(alarm_clock_toggle, alignment=Qt.AlignmentFlag.AlignRight)

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
