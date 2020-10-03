from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class PandasModel(QtCore.QAbstractTableModel):
    """
        Class to provide data by pandas dataFrame instance 
        Класс для предоставления данных из dataFrame
    """

    def __init__(self, data, parent=None):
        """
            Initialization of instance attributes including dataFrame. DataFrame is:
            two-dimensional size-mutable tabular data structure with labeled axes (rows and columns).
            Инициализация свойств экземпляра объекта, включая экземпляр данных dataFrame:
            DataFrame - Табличные данные в виде неизменяемого двумерного массива данных.
            Рамки обозначаются номерами строк и столбцов.
        """
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return str(section)
            if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
                return str(section)
        return None
