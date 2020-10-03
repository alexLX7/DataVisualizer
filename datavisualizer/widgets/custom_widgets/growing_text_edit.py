from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class GrowingTextEdit(QtWidgets.QTextEdit):
    """
        Class to manage interaction with resizable built-in QTextEdit instance
        Класс для управления размерами QTextEdit при взаимодействии с экземпляром класса 
    """

    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)
        self.height_min = 40
        self.height_max = 40
        self.number_of_chars = 50

    def sizeChange(self):
        doc_height = self.document().size().height()
        if self.height_min <= doc_height <= self.height_max:
            self.setMinimumHeight(doc_height)
        if len(self.document().toPlainText()) > self.number_of_chars:
            self.textCursor().deletePreviousChar()
