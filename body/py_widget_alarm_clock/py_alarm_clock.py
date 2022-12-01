from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QPushButton, QWidget, QGroupBox, QLabel, QHBoxLayout, QVBoxLayout

from body.py_widget_alarm_clock.py_toggle import PyToggle
from body.py_widget_alarm_clock.py_alarm_clock_setting import PyAlarmClockSetting


class PyAlarmClock(QWidget):
    def __init__(
            self,
            alarm_clock_area,
            time=QTime.currentTime(),
            family_fonts="Segoe UI",
            point_size=26,
            icon_day="icon_sun.png",
            icon_night="icon_moon.png",
            height_alarm_clock=100,
            width_alarm_clock=290,
    ):
        QWidget.__init__(self, alarm_clock_area)

        self._font_alarm_clock_time_enable = QFont()
        self._font_alarm_clock_time_enable.setFamily(family_fonts)
        self._font_alarm_clock_time_enable.setBold(True)
        self._font_alarm_clock_time_enable.setPointSize(point_size)

        self._font_alarm_clock_time_disable = QFont()
        self._font_alarm_clock_time_disable.setFamily(family_fonts)
        self._font_alarm_clock_time_disable.setPointSize(point_size)

        self._icon_day = QPixmap('body/image/' + icon_day)
        self._icon_night = QPixmap('body/image/' + icon_night)

        self.alarm_clock = QPushButton()
        self.alarm_clock.clicked.connect(self.clicked)
        self.alarm_clock.setMinimumSize(width_alarm_clock, height_alarm_clock)
        self.alarm_clock.setProperty("class", "alarm_clock")

        # CREAT THE AREA WITH THE ALARM TIME AND THE ICON, FOR LEFT ALIGNMENT
        self._space_for_time = QGroupBox(self.alarm_clock)
        self._space_for_time.setFixedSize(170, 80)
        self._space_for_time.setProperty("class", "space_for_time")

        self._alarm_clock_icon = QLabel(self._space_for_time)
        self._alarm_clock_icon.setPixmap(self._icon_day)

        self._alarm_clock_time = QLabel(time.toString("hh:mm"), self._space_for_time)
        self._alarm_clock_time.setFont(self._font_alarm_clock_time_enable)
        self._time = time

        self._alarm_clock_toggle = PyToggle()

        # ALIGN THE PICTURE AND THE TIME INSIDE THE BOX
        self._space_for_time_horizontal_layout = QHBoxLayout(self._space_for_time)
        self._space_for_time_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self._space_for_time_horizontal_layout.addWidget(self._alarm_clock_icon)
        self._space_for_time_horizontal_layout.addWidget(self._alarm_clock_time)

        # ALIGN OF ELEMENTS INSIDE THE WIDGET ALARM CLOCK
        self._alarm_clock_horizontal_layout = QHBoxLayout(self.alarm_clock)
        self._alarm_clock_horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self._alarm_clock_horizontal_layout.addWidget(self._space_for_time, alignment=Qt.AlignmentFlag.AlignLeft)
        self._alarm_clock_horizontal_layout.addWidget(self._alarm_clock_toggle, alignment=Qt.AlignmentFlag.AlignRight)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.alarm_clock)
        self.setLayout(layout)

    def setMinimumSize(self, minw: int, minh: int) -> None:
        self.alarm_clock.setMinimumSize(minw, minh)

    def setTime(self, time: QTime):
        self._alarm_clock_time.setText(time.toString("hh:mm"))
        self._time = time

    def enableAlarmClock(self):
        self._alarm_clock_toggle.setChecked(1)

    def settingAlarmClock(self):
        setting_alarm_clock = PyAlarmClockSetting(self, current_time=self._time)
        setting_alarm_clock.exec()

    def clicked(self):
        self.settingAlarmClock()
