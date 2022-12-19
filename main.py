import pickle
import sys

from PyQt6.QtCore import QSize, QRect, Qt, QTime, QTimer
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFrame, QStyleFactory
)

from header import Ui_Header
from body import Ui_Body


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.time_of_day = ['night', 'morning', 'day', 'evening']

        self.design_style = {
            'night': {
                'start_time': QTime(22, 0),
                'circle_bg': ('#000025', '#18054c'),
                'alarm_clock': ('#7a26c9', '#b641e6'),
                'toggle': ('#0faaff', '#330ba2'),
                'alarm_clock_setting': {
                    'bg_color': ('#220240', '#45206a'),
                    'bg_button': '#8a56bc'
                }
            },
            'morning': {
                'start_time': QTime(3, 0),
                'circle_bg': ('#7d1fdd', '#e9863d'),
                'alarm_clock': ('#e854a6', '#48e89c'),
                'toggle': ('#00bcff', '#777777'),
                'alarm_clock_setting': {
                    'bg_color': ('#a12469', '#b86646'),
                    'bg_button': '#36cf86'
                }
            },
            'day': {
                'start_time': QTime(9, 0),
                'circle_bg': ('#336cbb', '#fffa66'),
                'alarm_clock': ('#e018e7', '#1dd7e0'),
                'toggle': ('#00bcff', '#777777'),
                'alarm_clock_setting': {
                    'bg_color': ('#063f73', '#bf1dc5'),
                    'bg_button': '#a863ea'
                }
            },
            'evening': {
                'start_time': QTime(16, 0),
                'circle_bg': ('#c65909', '#3bc4a2'),
                'alarm_clock': ('#c24ae7', '#ece92a'),
                'toggle': ('#00bcff', '#777777'),
                'alarm_clock_setting': {
                    'bg_color': ('#982aba', '#56aa85'),
                    'bg_button': '#8a56bc'
                }
            }
        }

        self.current_time_of_day = 'night'

        # EXTERNAL CONTAINER
        self.container = QFrame()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # TO BE ABLE TO DRAG THE WINDOW
        self._old_pos = None

        self.circle_bg = QFrame(self.container)
        self.circle_bg.setGeometry(QRect(0, 0, 620, 620))
        self.circle_bg.setProperty("class", "circle_bg")
        self.circle_bg.setStyleSheet(".circle_bg {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
                                     "stop: 0 %s, stop: 1.0 %s)}" % ('#000025', '#18054c'))

        self.header = Ui_Header(self, self.circle_bg)
        self.body = Ui_Body(self.circle_bg, self.design_style)

        self.timer_change_style = QTimer()
        self.timer_change_style.timeout.connect(self.determiningNextStyleApplications)

        # setting window size
        self.setFixedSize(QSize(620, 620))

        # we install a frame with all the contents in the central widget
        self.setCentralWidget(self.container)

        self.determiningNextStyleApplications()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self._old_pos:
            return
        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def determiningNextStyleApplications(self):
        time_to_next_change = 24 * 60 * 60

        next_time_of_day = 1

        for time_of_day in range(len(self.time_of_day)):
            secs_to_next_time_of_day = QTime.secsTo(QTime.currentTime(),
                                                    self.design_style[self.time_of_day[time_of_day]]['start_time'])
            if time_to_next_change > secs_to_next_time_of_day > 0:
                time_to_next_change = secs_to_next_time_of_day
                next_time_of_day = time_of_day

        self.current_time_of_day = self.time_of_day[next_time_of_day - 1]

        self.changeStyleApplication(self.current_time_of_day)

        self.timer_change_style.setInterval(time_to_next_change * 1000)  # time in millisecond
        self.timer_change_style.start()

    def changeStyleApplication(self, time_of_day):
        self.circle_bg.setStyleSheet(".circle_bg {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
                                     "stop: 0 %s, stop: 1.0 %s)}" % (self.design_style[time_of_day]['circle_bg'][0],
                                                                     self.design_style[time_of_day]['circle_bg'][1]))

        self.body.changeStyleBody(time_of_day)

    def savingData(self):
        data_file = []
        with open("appdata", "wb") as appdata:
            for alarm_clock in self.body.list_alarm_clocks:
                data_alarm_clock = {
                    'time': alarm_clock.time,
                    'check_days_of_week': alarm_clock.check_days_of_week,
                    'music': alarm_clock.music
                }
                data_file.append(data_alarm_clock)
            pickle.dump(data_file, appdata)

    def close(self):
        self.savingData()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))

    window = MainWindow()
    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())
    window.show()
    app.exec()
