from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


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

        self.time_edit_area = QFrame()

        self.time_alarm_clock_label = QLabel("Время будильника:", self.time_edit_area)
        self.time_alarm_clock_setting = QTimeEdit(self.time_edit_area)

        self.horizontal_time_area_layout = QHBoxLayout(self.time_edit_area)
        self.horizontal_time_area_layout.addWidget(self.time_alarm_clock_label)
        self.horizontal_time_area_layout.addWidget(self.time_alarm_clock_setting)

        self.vertical_layout = QVBoxLayout(self.container)
        self.vertical_layout.addWidget(self.time_edit_area)

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
