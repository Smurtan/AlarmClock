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
    def __init__(self, application_class):
        super().__init__()

        self.time_of_day = ['night', 'morning', 'day', 'evening']
        self.application_class = application_class

        self.design_style = {
            'night': {
                'start_time': QTime(22, 0),
                'alarm_clock': ('#7a26c9', '#b641e6'),
                'toggle': ('#330ba2', '#0faaff'),
                'alarm_clock_setting': {
                    'bg_button': '#8a56bc'
                }
            },
            'morning': {
                'start_time': QTime(3, 0),
                'alarm_clock': ('#e854a6', '#48e89c'),
                'toggle': ('#8c2f63', '#00bcff'),
                'alarm_clock_setting': {
                    'bg_button': '#c26297'
                }
            },
            'day': {
                'start_time': QTime(9, 0),
                'alarm_clock': ('#e018e7', '#1dd7e0'),
                'toggle': ('#8f0a94', '#00bcff'),
                'alarm_clock_setting': {
                    'bg_button': '#9d3cd0'
                }
            },
            'evening': {
                'start_time': QTime(16, 0),
                'alarm_clock': ('#c24ae7', '#ece92a'),
                'toggle': ('#771197', '#0faaff'),
                'alarm_clock_setting': {
                    'bg_button': '#8a56bc'
                }
            }
        }

        self.current_time_of_day = self.time_of_day[0]

        # EXTERNAL CONTAINER
        self.container = QFrame()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # TO BE ABLE TO DRAG THE WINDOW
        self._old_pos = None

        self.circle_bg = QFrame(self.container)
        self.circle_bg.setGeometry(QRect(0, 0, 620, 620))
        self.circle_bg.setObjectName("circle_bg")

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
        if event.button() == Qt.MouseButton.RightButton and self.header.close_button.underMouse():
            self.close()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self._old_pos:
            return
        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def determiningNextStyleApplications(self) -> None:
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

    def changeStyleApplication(self, time_of_day: str) -> None:
        with open(f"Styles/{time_of_day}.qss", "r") as style_file:
            self.application_class.setStyleSheet(style_file.read())

        self.body.changeStyleBody(time_of_day)

    def savingData(self) -> None:
        data_file = []
        with open("appdata", "wb") as appdata:
            for alarm_clock in self.body.list_alarm_clocks:
                data_alarm_clock = {
                    'time': alarm_clock.time,
                    'check_days_of_week': alarm_clock.check_days_of_week,
                    'music': alarm_clock.music,
                    'condition_toggle': alarm_clock.alarm_clock_toggle.isChecked()
                }
                data_file.append(data_alarm_clock)
            pickle.dump(data_file, appdata)

    def minimizedWindow(self):
        self.showMinimized()

    def close(self) -> None:
        self.savingData()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))

    window = MainWindow(app)
    window.show()
    app.exec()
