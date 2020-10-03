from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datavisualizer.models.translation as translation


class CustomSqlDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.list_of_sql_table_names = self.parent.list_of_sql_table_names
        self.translation = translation.Translation()
        if self.list_of_sql_table_names:
            self.users_choice = self.list_of_sql_table_names[0]
            self.init()

    def init(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)

        self.title = self.translation.selected_language.get(
            'options', 'Options')
        self.setWindowTitle(self.title)
        self.setMinimumSize(QtCore.QSize(100, 100))
        self.setMaximumSize(QtCore.QSize(400, 400))

        button_color = QPushButton()
        button_color.setText("OK")

        def button_color_clicked(arg):
            self.parent.selected_sql_table = self.users_choice
            self.confirm_close_of_window()

        button_color.clicked.connect(button_color_clicked)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        button_color.setSizePolicy(sizePolicy)

        qVBoxLayout = QtWidgets.QVBoxLayout()

        combo_box = QComboBox()
        for each_type in self.list_of_sql_table_names:
            combo_box.addItem(each_type)

        combo_box.setCurrentIndex(
            self.list_of_sql_table_names.index(self.users_choice)
        )

        combo_box.activated[str].connect(self.set_type_of_plot)

        qVBoxLayout.addWidget(combo_box, alignment=QtCore.Qt.AlignTop)
        qVBoxLayout.addWidget(button_color, alignment=QtCore.Qt.AlignBottom)

        frame_2 = QtWidgets.QFrame()
        frame_2.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        frame_2.setLayout(qVBoxLayout)

        layout.addWidget(frame_2)

    def set_type_of_plot(self, text):
        self.users_choice = text

    def confirm_close_of_window(self):
        self.reject()

    def closeEvent(self, event):
        '''
            Method to filter out closeEvent out of all events and to call confirm_close_of_window().
            Метод для фильтрации события из всех событий для корректного вызова 
            метода confirm_close_of_window().
        '''
        event.ignore()
        self.confirm_close_of_window()
