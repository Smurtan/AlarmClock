import os

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from body.py_standard_button import PyStandardButton
from body.py_widget_alarm_clock.py_alarm_clock_setting.py_checkbox_day import PyCheckBoxDay


class PyAlarmClockSetting(QDialog):
    def __init__(
            self,
            alarm_clock,
            selected_time=QTime.currentTime(),
            selected_days_of_week=None,
            select_music: dict = None,
            first_color_bg_gradient='#220240',
            second_color_bg_gradient='#45206a',
            color_label='#ffffff'
    ):
        super().__init__(alarm_clock)

        self.move(alarm_clock.window().pos().x() + 50, alarm_clock.window().pos().y() + 120)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.container = QFrame()
        self.container.setFixedSize(500, 280)
        self.container.setProperty("class", "alarm_clock_setting")
        self.container.setStyleSheet(
            ".alarm_clock_setting {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
            "stop: 0 %s, stop: 1.0 %s)}" % (first_color_bg_gradient, second_color_bg_gradient))

        if selected_days_of_week is None:
            selected_days_of_week = [False for i in range(7)]

        self._alarm_clock = alarm_clock
        self._selected_days_of_week = selected_days_of_week

        self.time_alarm_clock_label = QLabel("Когда вы хотите меня услышать?")
        self.time_alarm_clock_label.setFont(QFont("Segoe UI", 22))
        self.time_alarm_clock_label.setStyleSheet(f'color: {color_label}')

        self.time_alarm_clock_setting = QTimeEdit()
        self.time_alarm_clock_setting.setTime(selected_time)
        self.time_alarm_clock_setting.setMinimumSize(90, 40)

        # DAYS OF WEEK
        self.area_days_of_week = QFrame()

        self.horizontal_days_of_week_layout = QHBoxLayout(self.area_days_of_week)

        self.checkbox_days = []
        for day in [('Пн', '#fff'), ('Вт', '#fff'), ('Ср', '#fff'), ('Чт', '#fff'),
                    ('Пт', '#fff'), ('Сб', '#fff'), ('Вс', '#ffffff')]:
            self.checkbox_days.append(PyCheckBoxDay(day[0], self.area_days_of_week, circle_color='#d4ae17',
                                                    text_color=day[1], active_text_color='#d4ae17'))
            self.horizontal_days_of_week_layout.addWidget(self.checkbox_days[-1])

        for day in range(7):
            self.checkbox_days[day].setChecked(self._selected_days_of_week[day])

        if not any(self._selected_days_of_week):
            self.checkbox_days[QDate.currentDate().dayOfWeek() - 1].setChecked(1)

        self.list_music = [file for file in os.listdir("Music")]

        self.music_combo = QComboBox(self.container)
        self.music_combo.setMaximumWidth(210)

        for music in self.list_music:
            self.music_combo.addItem(music)
        if select_music is not None:
            self.music_combo.setCurrentIndex(select_music['index'])

        self.button_box = QFrame(self.container)
        self.button_box.setFixedWidth(self.container.width() - 30)

        self.control_button = QFrame(self.button_box)
        self.control_button.setContentsMargins(0, 0, 0, 0)
        self.control_button.setProperty("class", "control_button")

        self.button_OK = PyStandardButton("OK", width=92, height=25, bg_color="#f6c608", text_color="#250246", point_size=18)
        self.button_OK.clicked.connect(self.acceptSetting)
        self.button_Cancel = PyStandardButton("Cancel", width=92, height=25, bg_color="#8a56bc",
                                              text_color="#ffffff", point_size=18)
        self.button_Cancel.clicked.connect(self.rejectSetting)

        self.horizontal_layout_control_button = QHBoxLayout(self.control_button)
        self.horizontal_layout_control_button.setSpacing(10)
        self.horizontal_layout_control_button.addWidget(self.button_OK)
        self.horizontal_layout_control_button.addWidget(self.button_Cancel)

        self.button_Delete = PyStandardButton("Delete", width=92, height=25, bg_color="#8a56bc",
                                              text_color="#ffffff", point_size=18)
        self.button_Delete.clicked.connect(self.removeAlarmClock)

        self.button_horizontal_layout = QHBoxLayout(self.button_box)
        self.button_horizontal_layout.addWidget(self.button_Delete, alignment=Qt.AlignmentFlag.AlignLeft)
        self.button_horizontal_layout.addWidget(self.control_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.vertical_layout = QVBoxLayout(self.container)
        self.vertical_layout.addWidget(self.time_alarm_clock_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.time_alarm_clock_setting, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.area_days_of_week, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.music_combo, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addWidget(self.button_box, alignment=Qt.AlignmentFlag.AlignHCenter)

        # set default
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)

    def acceptSetting(self) -> None:
        self._alarm_clock.setTimeAndIcon(self.time_alarm_clock_setting.time())
        self._alarm_clock.setMusic(self.list_music[self.music_combo.currentIndex()], self.music_combo.currentIndex())
        self._alarm_clock.enableAlarmClock()
        self._alarm_clock.setDaysOfWeek(self.checkbox_days)
        self._alarm_clock.body.determiningNextAlarmClock()
        self.accept()

    def rejectSetting(self) -> None:
        # IF THE CANCELLATION OCCURRED BEFORE THE ALARM WAS CREATED
        if not any(self._selected_days_of_week):
            self.removeAlarmClock()
        else:
            self.reject()

    def removeAlarmClock(self) -> None:
        self._alarm_clock.removeAlarmClock()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = PyAlarmClockSetting()
    window.show()
    app.exec()
