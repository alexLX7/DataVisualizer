import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datavisualizer.models.translation as translation


class HelpWindow(QtWidgets.QMainWindow):
    """
        Class to help users get into the interface and the usage of the program
        Класс, предназначенный для помощи пользователю при работе с программой
    """

    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent)
        self.init()

    def init(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        widget.setLayout(layout)

        self.translation = translation.Translation()
        self.title = self.translation.selected_language.get('help', 'Help')
        self.left = 100
        self.top = 100
        self.windowWidth = 300
        self.windowHeight = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top,
                         self.windowWidth, self.windowHeight)

        font = QtGui.QFont()
        font.setPointSize(11)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)

        label_text = QLabel()
        label_text.setText(
            self.translation.selected_language.get('help', 'Help')
        )
        vbox.addWidget(label_text)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)

        text = 'datavisualizer/resources/help/help.txt\n\n'
        text_edit.setText(text)
        try:
            with open(
                os.path.join(os.getcwd(), 'datavisualizer', 'resources', 'help', 'help.txt'), encoding='utf-8'
            ) as file:
                text = file.read()
                text_edit.append(text)
        except:
            pass

        vbox.addWidget(text_edit)

        layout.addWidget(frame)
