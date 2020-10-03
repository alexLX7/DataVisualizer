from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datavisualizer.models.translation as translation


class GlobalInfo:
    def __init__(self, text_to_show):
        super(GlobalInfo, self).__init__()
        self.translation = translation.Translation()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText(str(text_to_show))
        msg.setWindowTitle(
            self.translation.selected_language.get(
                'information', 'Information')
        )
        msg.exec_()
