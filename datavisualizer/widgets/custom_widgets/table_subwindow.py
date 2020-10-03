from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TableSubWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TableSubWindow, self).__init__(parent)
        self._want_to_close = False

    def closeEvent(self, evnt):
        if self._want_to_close:
            super(TableSubWindow, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.setWindowState(QtCore.Qt.WindowMinimized)
