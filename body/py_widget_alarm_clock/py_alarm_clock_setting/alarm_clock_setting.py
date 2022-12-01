from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from body.py_widget_alarm_clock.py_alarm_clock_setting.py_checkbox_day import PyCheckBoxDay


class PyAlarmClockSetting(QDialog):
    def __init__(
            self,
            alarm_clock=None,
            current_time=QTime.currentTime(),
            current_day_of_week=QDate.currentDate().dayOfWeek()
    ):
        super().__init__(alarm_clock)
        self._alarm_clock = alarm_clock

        self.setWindowTitle("Alarm Clock")

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.acceptSetting)
        self.button_box.rejected.connect(self.rejectSetting)

        self.container = QFrame()

        self.time_alarm_clock_label = QLabel("Когда вы хотите меня услышать?")
        self.time_alarm_clock_label.setFont(QFont("Segoe UI", 20))

        self.time_alarm_clock_setting = QTimeEdit()
        self.time_alarm_clock_setting.setTime(current_time)
        self.time_alarm_clock_setting.setMinimumSize(90, 40)

        # DAYS OF WEEK
        self.area_days_of_week = QFrame()

        self.horizontal_days_of_week_layout = QHBoxLayout(self.area_days_of_week)

        self.checkbox_days = []
        for day in [('Пн', '#0'), ('Вт', '#0'), ('Ср', '#0'), ('Чт', '#0'),
                    ('Пт', '#0'), ('Сб', '#0'), ('Вс', '#ff0000')]:
            self.checkbox_days.append(PyCheckBoxDay(day[0], self.area_days_of_week, text_color=day[1]))
            self.horizontal_days_of_week_layout.addWidget(self.checkbox_days[-1])

        self.checkbox_days[current_day_of_week - 1].setChecked(1)

        self.vertical_layout = QVBoxLayout(self.container)
        self.vertical_layout.addWidget(self.time_alarm_clock_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.time_alarm_clock_setting, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.area_days_of_week, alignment=Qt.AlignmentFlag.AlignHCenter)

        # set default
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.container)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def acceptSetting(self) -> None:
        self._alarm_clock.setTime(self.time_alarm_clock_setting.time())
        self._alarm_clock.enableAlarmClock()
        self.accept()

    def rejectSetting(self) -> None:
        self.reject()


if __name__ == '__main__':
    app = QApplication([])
    window = PyAlarmClockSetting()
    window.show()
    app.exec()
