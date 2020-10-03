from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ProjectInstanceWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ProjectInstanceWidget, self).__init__()
        self.label_for_name = QtWidgets.QLabel()
        self.label_for_additional_info = QtWidgets.QLabel()
        self.label_for_icon = QtWidgets.QLabel()
        self.qVBoxLayout = QtWidgets.QVBoxLayout()
        self.qHBoxLayout = QtWidgets.QHBoxLayout()
        self.qVBoxLayout.addWidget(self.label_for_name)
        self.qVBoxLayout.addWidget(self.label_for_additional_info)
        self.qHBoxLayout.addWidget(self.label_for_icon, 0)
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

    def set_label_for_icon(self, image_path):
        self.label_for_icon.setPixmap(QtGui.QPixmap(image_path))
