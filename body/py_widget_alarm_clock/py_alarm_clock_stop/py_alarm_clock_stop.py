import vlc
import winsound

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from body.py_standard_button import PyStandardButton
from body.py_widget_alarm_clock import PyAlarmClock


class PyAlarmClockStop(QDialog):
    def __init__(
            self,
            sound: str = None
    ):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._sound = vlc.MediaPlayer("Music/" + sound)

        self.stop_button = PyStandardButton("STOP!", width=190, height=70, bg_color='#fed402', text_color='000',
                                            point_size=50)
        self.stop_button.clicked.connect(self.closeEvent)

        try:
            self._sound.play()
        except AttributeError:
            winsound.PlaySound("SystemHand", winsound.SND_LOOP)
            print('Вы потеряли песню!')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stop_button)
        self.setLayout(self.layout)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self._sound.stop()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = PyAlarmClockStop()
    window.show()
    app.exec()
