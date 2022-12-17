import vlc

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from body.py_standard_button import PyStandardButton


class PyAlarmClockStop(QDialog):
    def __init__(
            self,
            alarm_clock=None,
            sound=None
    ):
        super().__init__(alarm_clock)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._alarm_clock = alarm_clock
        self.sound = vlc.MediaPlayer("Music/" + sound)

        self.stop_button = PyStandardButton("STOP!", width=190, height=70, bg_color='#fed402', text_color='000',
                                            point_size=50)
        self.stop_button.clicked.connect(self.closeEvent)

        try:
            self.sound.play()
        except AttributeError:
            print('Вы потеряли песню!')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stop_button)
        self.setLayout(self.layout)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.sound.stop()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = PyAlarmClockStop()
    window.show()
    app.exec()
