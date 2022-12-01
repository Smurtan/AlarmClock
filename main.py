import sys

from PyQt6 import QtGui
from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFrame, QLabel,
    QVBoxLayout, QScrollArea
)

from header import Ui_Header
from body import Ui_Body


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # EXTERNAL CONTAINER
        self.container = QFrame()

        self.circle_bg = QFrame(self.container)
        self.circle_bg.setGeometry(QRect(0, 0, 620, 620))
        self.circle_bg.setProperty("class", "circle_bg")

        self.body = Ui_Body(self.circle_bg)
        self.header = Ui_Header(self.circle_bg)

        # setting window size
        self.setFixedSize(QSize(620, 620))

        # we install a frame with all the contents in the central widget
        self.setCentralWidget(self.container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    window.show()

    app.exec()
