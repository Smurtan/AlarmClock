import pickle

from PyQt6.QtCore import Qt, QRect, QTimer, QTime, QDate
from PyQt6.QtWidgets import (QWidget, QFrame, QScrollArea,
                             QVBoxLayout)

from body.py_widget_alarm_clock import PyAlarmClock
from body.custom_button import PyAddButton
from body.py_widget_alarm_clock.py_alarm_clock_stop import PyAlarmClockStop


class Ui_Body:
    def __init__(
            self,
            parent: QWidget,
            design_style: dict = None
    ):
        self.design_style = design_style
        self.time_of_day = 'night'  # standard

        # перенести в .ini
        self.height_alarm_clock = 100
        self.spacing_alarm_clock = 20

        self.alarm_clocks_area = QFrame()
        self.alarm_clocks_area.setGeometry(QRect(0, 0, 620, 340))
        self.alarm_clocks_area.setObjectName("alarm_clocks_area")

        self.alarm_clocks_scroll_area = QScrollArea(parent)
        self.alarm_clocks_scroll_area.setGeometry(QRect(0, 230, 620, 340))
        self.alarm_clocks_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_clocks_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.alarm_clocks_scroll_area.setObjectName("alarm_clocks_scroll_area")
        self.alarm_clocks_scroll_area.setWidget(self.alarm_clocks_area)

        self.vertical_layout_alarm_clocks = QVBoxLayout(self.alarm_clocks_area)
        self.vertical_layout_alarm_clocks.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_alarm_clocks.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vertical_layout_alarm_clocks.setSpacing(self.spacing_alarm_clock)

        # INITIALIZATION OF CREATED ALARMS
        self.list_alarm_clocks = []
        try:
            with open("appdata", "rb") as appdata:
                self.list_data_alarm_clock = pickle.load(appdata)
                for alarm_clock in range(len(self.list_data_alarm_clock)):
                    self.list_alarm_clocks.append(PyAlarmClock(
                        self,
                        self.alarm_clocks_area,
                        self.list_alarm_clocks,
                        self.list_data_alarm_clock[alarm_clock]['time'],
                        self.list_data_alarm_clock[alarm_clock]['check_days_of_week'],
                        self.list_data_alarm_clock[alarm_clock]['music'],
                        self.list_data_alarm_clock[alarm_clock]['condition_toggle'],
                        height_alarm_clock=self.height_alarm_clock
                    ))
                    # EACH ALARM CLOCKS IS ALIGNED SEPARATELY, AS IT HAS ITS OWN SIZE
                    self.vertical_layout_alarm_clocks.addWidget(self.list_alarm_clocks[-1],
                                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        except (FileNotFoundError, EOFError):
            print('Вы потеряли файл с данными!')

        # SETTING PARAMETERS FOR THE IMPLEMENTATION OF CHANGING THE SIZE OF ALARMS
        self.scroll_value = 0
        self.last_scroll = 0  # will be used to determine the scrolling direction
        self.last_count_alarm_clocks = 0
        self.alarm_clocks_scroll_area.verticalScrollBar().valueChanged.connect(self.changingWidthAlarmClock)

        # AUTOMATICALLY CHANGE THE WIDTH OF ALL ALARM CLOCKS
        self.changingWidthAlarmClock(0)
        # THE WIDTH OF THE AREA ADJUSTS TO THE NUMBER OF ALARM CLOCKS
        self.changeHeightAlarmClockArea()

        self.new_alarm_clock_button = PyAddButton(parent)
        self.new_alarm_clock_button.setGeometry(160, 572, 300, 40)
        self.new_alarm_clock_button.clicked.connect(self.addNewAlarmClock)

        self.timer_next_alarm_clock = QTimer()
        self.timer_next_alarm_clock.timeout.connect(self.callingAlarmClock)

        self.serial_number_nearest_alarm_clock = None
        self.determiningNextAlarmClock()

    def changeHeightAlarmClockArea(self) -> None:
        self.alarm_clocks_area.setGeometry(QRect(0, 0, 620, (len(self.list_alarm_clocks) - 1) * (
                self.height_alarm_clock + self.spacing_alarm_clock) + self.height_alarm_clock))

    def determiningNextAlarmClock(self) -> None:
        time_to_nearest_alarm_clock = 24 * 60 * 60
        current_day_of_week = QDate.currentDate().dayOfWeek() - 1

        for alarm_clock in self.list_alarm_clocks:
            if alarm_clock.check_days_of_week[current_day_of_week]:
                time_to_alarm_clock = QTime.secsTo(QTime.currentTime(), alarm_clock.time)
                if (0 < time_to_alarm_clock < time_to_nearest_alarm_clock and
                        QTime.currentTime().minute() != alarm_clock.time.minute()):
                    # to make the alarm clock sing at the beginning of the desired minute
                    time_to_nearest_alarm_clock = time_to_alarm_clock // 60 + (60 - QTime.currentTime().second())
                    self.serial_number_nearest_alarm_clock = alarm_clock.serial_number

        self.timer_next_alarm_clock.setInterval(time_to_nearest_alarm_clock * 1000)  # time in millisecond
        self.timer_next_alarm_clock.start()

    def addNewAlarmClock(self) -> None:
        new_alarm_clock = PyAlarmClock(self, self.alarm_clocks_area, self.list_alarm_clocks,
                                       height_alarm_clock=self.height_alarm_clock
                                       )
        self.list_alarm_clocks.append(new_alarm_clock)

        self.changeHeightAlarmClockArea()

        # THE ALARM WILL BE ADDED IF THE USER CLICKS OK
        if new_alarm_clock.openingAlarmClockSettingWindow():
            self.vertical_layout_alarm_clocks.addWidget(new_alarm_clock,
                                                        alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

            self.changingWidthAlarmClock(self.last_scroll // 60 * 60)
            self.determiningNextAlarmClock()

    def determiningDirectionScrolling(self, scrolled_pixels: int) -> int:
        if self.last_scroll < scrolled_pixels:
            return 1  # down
        else:
            return 0  # up

    def changeVisibleAlarmClocks(self, count_alarm_clocks: int, first_visible_alarm_clock: int,
                                 scroll_direction: int) -> None:
        # +4 TO THE FIRST VISIBLE ALARM CLOCK HELPS TO DETERMINE WHEN 4 ALARMS ARE VISIBLE IN THE FIELD
        if count_alarm_clocks >= first_visible_alarm_clock + 4:
            self.visible_alarm_clock = self.list_alarm_clocks[first_visible_alarm_clock + scroll_direction:
                                                              first_visible_alarm_clock + scroll_direction + 3]
        else:
            self.visible_alarm_clock = self.list_alarm_clocks[first_visible_alarm_clock:]

    def changingWidthAlarmClock(self, scrolled_pixels: int) -> None:
        count_scroll = scrolled_pixels // 60
        first_visible_alarm_clock = scrolled_pixels // 120
        count_alarm_clocks = len(self.list_alarm_clocks)

        scroll_direction = self.determiningDirectionScrolling(scrolled_pixels)
        count_scroll -= scroll_direction * -1  # so that the size changes correctly when scrolling down

        self.last_scroll = scrolled_pixels

        # THE LIST OF VISIBLE ALARMS CHANGES ONLY WHEN 3 WHOLE ALARMS ARE VISIBLE
        if (count_scroll + 1) % 2 != 0:
            self.changeVisibleAlarmClocks(count_alarm_clocks, first_visible_alarm_clock, scroll_direction)

        if self.last_count_alarm_clocks > count_alarm_clocks:
            self.changeHeightAlarmClockArea()
            self.changeVisibleAlarmClocks(count_alarm_clocks, first_visible_alarm_clock, scroll_direction)

        self.last_count_alarm_clocks = count_alarm_clocks

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

    def callingAlarmClock(self) -> None:
        if self.list_alarm_clocks[self.serial_number_nearest_alarm_clock].alarm_clock_toggle.isChecked():
            stop_widget = PyAlarmClockStop(self.list_alarm_clocks[self.serial_number_nearest_alarm_clock],
                                           self.list_alarm_clocks[self.serial_number_nearest_alarm_clock].music[
                                               'music'])
            stop_widget.exec()

        self.determiningNextAlarmClock()

    def changeStyleBody(self, time_of_day: str) -> None:
        self.time_of_day = time_of_day

        for alarm_clock in self.list_alarm_clocks:
            alarm_clock.changeStyleAlarmClock(time_of_day)
