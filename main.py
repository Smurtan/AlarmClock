import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
QMainWindow, QApplication, QFrame
)


class MainWindow(QMainWindow):

    """The class describes the main application window"""

    def __init__(self):

        """Contains settings of the main window and widgets"""

        super(MainWindow, self).__init__()

        # window size
        self.setMinimumSize(QSize(620, 620))
        self.setMaximumSize(QSize(620, 620))

        # external content container
        self.container = QFrame()
        self.container.setContentsMargins(10, 10, 10, 10)
        # ?
        self.container.setFrameShape(QFrame.Shape.NoFrame)
        self.container.setFrameShadow(QFrame.Shadow.Raised)

        self.circle_bg = QFrame(self.container)
        self.circle_bg.setMinimumSize(QSize(610, 610))
        self.circle_bg.setMaximumSize(QSize(610, 610))
        self.circle_bg.setContentsMargins(20, 20, 20, 20)
        # ?
        self.circle_bg.setFrameShape(QFrame.Shape.NoFrame)
        self.circle_bg.setFrameShadow(QFrame.Shadow.Raised)

        self.setCentralWidget(self.container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    with open("styles.css", "r") as file:
        app.setStyleSheet(file.read())
    window.show()

    app.exec()
