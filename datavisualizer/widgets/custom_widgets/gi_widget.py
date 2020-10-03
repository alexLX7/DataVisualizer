from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datavisualizer.models.translation as translation


class GraphicsInstanceWidget(QtWidgets.QWidget):
    def __init__(self):
        super(GraphicsInstanceWidget, self).__init__()
        self.translation = translation.Translation()
        self.label_for_name = QtWidgets.QLabel()
        self.label_for_additional_info = QtWidgets.QLabel()
        self.label_for_visibility = QtWidgets.QLabel()
        self.label_for_color = QtWidgets.QLabel()
        self.label_for_color.setFixedSize(60, 60)
        self.qVBoxLayout = QtWidgets.QVBoxLayout()
        self.qHBoxLayout = QtWidgets.QHBoxLayout()
        self.qVBoxLayout.addWidget(self.label_for_name)
        self.qVBoxLayout.addWidget(self.label_for_additional_info)
        self.qVBoxLayout.addWidget(self.label_for_visibility)
        self.qHBoxLayout.addWidget(self.label_for_color, 0)
        self.qHBoxLayout.addLayout(self.qVBoxLayout, 1)
        self.frame = QtWidgets.QFrame()
        self.frame.setFrameStyle(
            QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        self.frame.setLayout(self.qHBoxLayout)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.frame)
        self.setLayout(self.layout)

    def set_label_for_additional_info(self, text):
        self.label_for_additional_info.setText(str(text))

    def set_label_for_name(self, text):
        self.label_for_name.setText(str(text))

    def set_label_for_visibility(self, is_visible):
        if is_visible:
            self.label_for_visibility.setText('(' +
                                              str(self.translation.selected_language.get('shown', 'shown')) + ')')
        else:
            self.label_for_visibility.setText('(' +
                                              str(self.translation.selected_language.get('hidden', 'hidden')) + ')')

    def set_label_for_color(self, color):
        self.label_for_color.setStyleSheet(
            "background-color:" + str(color) + ";color: black;")
