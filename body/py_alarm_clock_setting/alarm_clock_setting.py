from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from body.py_alarm_clock_setting.py_checkbox_day import PyCheckBoxDay


class AlarmClockSetting(QDialog):
    def __init__(
            self,
            parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle("Alarm Clock")

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.container = QFrame()

        # TIME EDIT
        self.time_edit_area = QFrame()

        self.time_alarm_clock_label = QLabel("Когда вы хотите меня услышать?", self.time_edit_area)
        self.time_alarm_clock_setting = QTimeEdit(self.time_edit_area)

        self.horizontal_time_area_layout = QHBoxLayout(self.time_edit_area)
        self.horizontal_time_area_layout.addWidget(self.time_alarm_clock_label)
        self.horizontal_time_area_layout.addWidget(self.time_alarm_clock_setting)

        # DAYS OF WEEK
        self.area_days_of_week = QFrame()

        self.checkbox_monday = PyCheckBoxDay("Пн", self.area_days_of_week)
        self.checkbox_tuesday = PyCheckBoxDay("Вт", self.area_days_of_week)
        self.checkbox_wednesday = PyCheckBoxDay("Ср", self.area_days_of_week)
        self.checkbox_thursday = PyCheckBoxDay("Чт", self.area_days_of_week)
        self.checkbox_friday = PyCheckBoxDay("Пт", self.area_days_of_week)
        self.checkbox_saturday = PyCheckBoxDay("Сб", self.area_days_of_week)
        self.checkbox_sunday = PyCheckBoxDay("Вс", self.area_days_of_week)
        # в список

        self.horizontal_days_of_week_layout = QHBoxLayout(self.area_days_of_week)
        self.horizontal_days_of_week_layout.addWidget(self.checkbox_monday)
        self.horizontal_days_of_week_layout.addWidget(self.checkbox_tuesday)
        self.horizontal_days_of_week_layout.addWidget(self.checkbox_wednesday)
        self.horizontal_days_of_week_layout.addWidget(self.checkbox_thursday)
        self.horizontal_days_of_week_layout.addWidget(self.checkbox_friday)
        self.horizontal_days_of_week_layout.addWidget(self.checkbox_saturday)
        self.horizontal_days_of_week_layout.addWidget(self.checkbox_sunday)

        self.vertical_layout = QVBoxLayout(self.container)
        self.vertical_layout.addWidget(self.time_edit_area)
        self.vertical_layout.addWidget(self.area_days_of_week)

        # set default
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.container)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication([])
    window = AlarmClockSetting()
    window.show()
    app.exec()
