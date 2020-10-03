from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datavisualizer.models.translation as translation


class AboutWindow(QtWidgets.QMainWindow):
    """
        Class to introduce general purpose of the program and information about the creator
        Класс для представления назначения данной программы и информации об авторе
    """

    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.init()

    def init(self):
        self.translation = translation.Translation()
        self.title = self.translation.selected_language.get(
            "about_window_title", "About")
        self.left = 100
        self.top = 100
        self.windowWidth = 300
        self.windowHeight = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top,
                         self.windowWidth, self.windowHeight)
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        widget.setLayout(layout)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)

        label_creator_name = QLabel()
        creator_name = self.translation.selected_language.get(
            'about_window_creators_name', 'Pavlov Alex')
        label_creator_name.setText(creator_name)
        vbox.addWidget(label_creator_name)

        label_creator_github = QLabel()
        creator_github = self.translation.selected_language.get(
            'about_window_creators_github', 'https://github.com/alexLX7')
        label_creator_github.setText(creator_github)
        vbox.addWidget(label_creator_github)

        vbox.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(frame)
