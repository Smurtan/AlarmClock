from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .py_toggle import PyToggle


class PyAlarmClock(QWidget):
    def __init__(
            self,
            alarm_clock_area,
            time="00:00",
            family_fonts="Segoe UI",
            point_size=26,
            icon_day="icon_sun.png",
            icon_night="icon_moon.png",
            min_height_alarm_clock=100,
            min_width_alarm_clock=290,
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
        self.icon_day = QPixmap('body/image/' + icon_day)
        self.icon_night = QPixmap('body/image/' + icon_night)

        # CREATE NEW ALARM CLOCK
        self.alarm_clock = QFrame(alarm_clock_area)
        self.alarm_clock.setMinimumSize(min_width_alarm_clock, min_height_alarm_clock)
        self.alarm_clock.setProperty("class", "alarm_clock")

        # CREAT THE AREA WITH THE ALARM TIME AND THE ICON, FOR LEFT ALIGNMENT
        space_for_time = QGroupBox(self.alarm_clock)
        space_for_time.setFixedSize(170, 80)
        space_for_time.setProperty("class", "space_for_time")

        # SET ICON
        alarm_clock_icon = QLabel(space_for_time)
        alarm_clock_icon.setPixmap(self.icon_day)

        # SET TIME
        alarm_clock_time = QLabel(time, space_for_time)
        alarm_clock_time.setFont(self.font_alarm_clock_time_enable)

        # CREAT TOGGLE
        alarm_clock_toggle = PyToggle()

        # ALIGN THE PICTURE AND THE TIME INSIDE THE ALARM CLOCK
        space_for_time_horizontal_layout = QHBoxLayout(space_for_time)
        space_for_time_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        space_for_time_horizontal_layout.addWidget(alarm_clock_icon)
        space_for_time_horizontal_layout.addWidget(alarm_clock_time)

        # ALIGN OF ELEMENTS INSIDE THE WIDGET ALARM CLOCK
        alarm_clock_horizontal_layout = QHBoxLayout(self.alarm_clock)
        alarm_clock_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        alarm_clock_horizontal_layout.addWidget(space_for_time, alignment=Qt.AlignmentFlag.AlignLeft)
        alarm_clock_horizontal_layout.addWidget(alarm_clock_toggle, alignment=Qt.AlignmentFlag.AlignRight)
