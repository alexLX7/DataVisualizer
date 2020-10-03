from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class OpeningWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(OpeningWindow, self).__init__(parent)
        self.init()

    def init(self):
        self.init_names()
        self.init_widgets()
        self.init_layout()
        self.init_window()

    def init_window(self):
        self.setWindowTitle('DataVisualizer')
        self.windowWidth = 380
        self.windowHeight = 260
        self.setFixedSize(self.windowWidth, self.windowHeight)

    def init_names(self):
        self.english = 'English'
        self.russian = 'Русский'
        self.english_json = 'english'
        self.russian_json = 'russian'
        self.english_continue = 'Continue'
        self.russian_continue = 'Продолжить'
        self.english_welcome = 'Welcome!\n\n\nSelect the language:'
        self.russian_welcome = 'Добро пожаловать!\n\n\nВыберите язык:'
        self.language = self.english_json

    def init_widgets(self):
        self.label_welcome = QtWidgets.QLabel(self.english_welcome)
        self.label_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.radio_button_english = QRadioButton(self.english)
        self.radio_button_english.setChecked(True)
        self.radio_button_english._language = self.english_json
        self.radio_button_english._welcome = self.english_welcome
        self.radio_button_english._continue = self.english_continue
        self.radio_button_english.toggled.connect(self.radio_button_changed)
        self.radio_button_russian = QRadioButton(self.russian)
        self.radio_button_russian._language = self.russian_json
        self.radio_button_russian._welcome = self.russian_welcome
        self.radio_button_russian._continue = self.russian_continue
        self.radio_button_russian.toggled.connect(self.radio_button_changed)
        self.accept_button = QtWidgets.QPushButton(self.english_continue)
        self.accept_button.clicked.connect(self.accept_button_clicked)

    def init_layout(self):
        self.qVBoxLayout = QtWidgets.QVBoxLayout()
        self.qVBoxLayout.addWidget(
            self.label_welcome, alignment=QtCore.Qt.AlignTop)
        self.qVBoxLayout.addWidget(
            self.radio_button_english, alignment=QtCore.Qt.AlignBottom)
        self.qVBoxLayout.addWidget(
            self.radio_button_russian, alignment=QtCore.Qt.AlignBottom)
        self.qVBoxLayout.addWidget(
            self.accept_button, alignment=QtCore.Qt.AlignBottom)
        self.frame = QtWidgets.QFrame()
        self.frame.setFrameStyle(
            QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        self.frame.setLayout(self.qVBoxLayout)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)

    def radio_button_changed(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.language = radio_button._language
            self.label_welcome.setText(radio_button._welcome)
            self.accept_button.setText(radio_button._continue)

    def accept_button_clicked(self):
        self.accept()
