from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datavisualizer.models.translation as translation
import datavisualizer.widgets.custom_widgets.growing_text_edit as gte


class CustomDialogOfGraphicsInstance(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.dynamically_changeable_gi = self.parent.dynamically_changeable_gi
        self.translation = translation.Translation()
        self.list_of_choices = [
            self.translation.selected_language.get(
                'choice_0', 'choice 0 is: x:x, y:y, z:z'),
            self.translation.selected_language.get(
                'choice_1', 'choice 1 is: x:y, y:x, z:z'),
            self.translation.selected_language.get(
                'choice_2', 'choice 2 is: x:z, y:y, z:x'),
            self.translation.selected_language.get(
                'choice_3', 'choice 3 is: x:z, y:x, z:y'),
            self.translation.selected_language.get(
                'choice_4', 'choice 4 is: x:x, y:z, z:y'),
            self.translation.selected_language.get(
                'choice_5', 'choice 5 is: x:y, y:z, z:x')
        ]
        self.users_choice = self.list_of_choices[
            self.dynamically_changeable_gi.index_of_users_choice_in_options_of_list_to_show
        ]
        self.init()

    def init(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)

        self.title = self.translation.selected_language.get(
            'options', 'Options')
        self.left = 100
        self.top = 100
        self.windowWidth = 800
        self.windowHeight = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top,
                         self.windowWidth, self.windowHeight)
        self.setMinimumSize(QtCore.QSize(500, 500))

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        layout.addWidget(scroll)
        scrollContents = QtWidgets.QWidget()
        scroll.setWidget(scrollContents)

        textLayout = QtWidgets.QVBoxLayout(scrollContents)
        font = QtGui.QFont()
        font.setPointSize(11)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        vbox = QtWidgets.QVBoxLayout()
        frame.setLayout(vbox)

        label_axis_x_y_z = QtWidgets.QLabel()
        label_axis_x_y_z.setText(
            self.translation.selected_language.get('original_lists_of_data',
                                                   'Original lists of data: axis x, axis y, axis z:')
        )
        vbox.addWidget(label_axis_x_y_z)

        label_number_of_values_of_each_axis = QtWidgets.QLabel()
        label_number_of_values_of_each_axis.setText(
            self.translation.selected_language.get('number_of_values_of_each_axis',
                                                   'Number of values of each axis:') + ' ' +
            str(self.dynamically_changeable_gi.number_of_values_of_axis_x) + ', ' +
            str(self.dynamically_changeable_gi.number_of_values_of_axis_x) + ', ' +
            str(self.dynamically_changeable_gi.number_of_values_of_axis_x) + '.'
        )
        vbox.addWidget(label_number_of_values_of_each_axis)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        text_edit_axis_x = QtWidgets.QTextEdit()
        text_edit_axis_x.setSizePolicy(sizePolicy)
        text_edit_axis_x.setText(
            str('\n\n'.join([',\t'.join([str(cell) for cell in row])
                             for row in self.dynamically_changeable_gi.final_list_of_x_y_z[0]])))
        text_edit_axis_x.setReadOnly(True)
        vbox.addWidget(text_edit_axis_x)

        text_edit_axis_y = QtWidgets.QTextEdit()
        text_edit_axis_y.setSizePolicy(sizePolicy)
        text_edit_axis_y.setText(
            str('\n\n'.join([',\t'.join([str(cell) for cell in row])
                             for row in self.dynamically_changeable_gi.final_list_of_x_y_z[1]])))
        text_edit_axis_y.setReadOnly(True)
        vbox.addWidget(text_edit_axis_y)

        text_edit_axis_z = QtWidgets.QTextEdit()
        text_edit_axis_z.setSizePolicy(sizePolicy)
        text_edit_axis_z.setText(
            str('\n\n'.join([',\t'.join([str(cell) for cell in row])
                             for row in self.dynamically_changeable_gi.final_list_of_x_y_z[2]])))
        text_edit_axis_z.setReadOnly(True)
        vbox.addWidget(text_edit_axis_z)

        splitter_1 = QSplitter(QtCore.Qt.Vertical)
        splitter_1.addWidget(text_edit_axis_x)
        splitter_1.addWidget(text_edit_axis_y)
        splitter_1.setStretchFactor(1, 10)
        splitter_1.setChildrenCollapsible(False)
        vbox.addWidget(splitter_1)

        splitter_2 = QSplitter(QtCore.Qt.Vertical)
        splitter_2.addWidget(splitter_1)
        splitter_2.addWidget(text_edit_axis_z)
        splitter_2.setStretchFactor(1, 10)
        splitter_2.setChildrenCollapsible(False)
        vbox.addWidget(splitter_2)

        label_table_name = QtWidgets.QLabel()
        label_for_additional_info = QtWidgets.QLabel()

        button_color = QPushButton()
        button_color.setText("\t" + self.translation.selected_language.get(
            'push_to_change_color', 'Push to change the color') + "\t")
        button_color.setStyleSheet(
            "background-color:" +
            str(self.dynamically_changeable_gi.color) +
            ";color: black;border: none;"
        )

        def button_color_clicked(arg):
            color = QtWidgets.QColorDialog.getColor()
            if color.isValid():
                self.dynamically_changeable_gi.color = color.name()
                button_color.setStyleSheet(
                    "background-color:" + str(color.name()) + ";color: black;border: none;")

        button_color.clicked.connect(button_color_clicked)

        label_for_additional_info.setText(
            self.translation.selected_language.get('number_of_instance', 'Number of instance') + ': ' +
            str(self.dynamically_changeable_gi.unique_id)
        )
        label_table_name.setText(
            self.translation.selected_language.get('table_name_of_selected_cells', 'Table name of selected cells') + ': ' +
            str(self.dynamically_changeable_gi.table_name)
        )

        checkbox_visible = QCheckBox()
        checkbox_visible.setText(
            self.translation.selected_language.get('visible', 'Visible'))
        checkbox_visible.setChecked(self.dynamically_changeable_gi.visible)

        def checkbox_visible_clicked(arg):
            if checkbox_visible.isChecked():
                self.dynamically_changeable_gi.visible = True
            else:
                self.dynamically_changeable_gi.visible = False

        checkbox_visible.toggled.connect(checkbox_visible_clicked)

        custom_growing_text_edit_for_name = gte.GrowingTextEdit()
        custom_growing_text_edit_for_name.setText(
            str(self.dynamically_changeable_gi.name))
        custom_growing_text_edit_for_name.setMinimumHeight(27)
        custom_growing_text_edit_for_name.setMaximumHeight(27)

        def custom_growing_text_edit_for_name_changed():
            try:
                self.dynamically_changeable_gi.name = custom_growing_text_edit_for_name.toPlainText()
            except:
                self.dynamically_changeable_gi.name = 'Incorrect symbols in name'

        custom_growing_text_edit_for_name.textChanged.connect(
            custom_growing_text_edit_for_name_changed)

        original_type_of_creation = QtWidgets.QLabel()
        original_type_of_creation.setText(
            self.translation.selected_language.get('original_type_of_creation',
                                                   'Original type of creation') + ': ' +
            str(self.dynamically_changeable_gi.original_type_of_creation)
        )

        original_file_name = QtWidgets.QLabel()
        original_file_name.setText(
            self.translation.selected_language.get('original_file_name', 'Original file name') + ': ' +
            str(self.dynamically_changeable_gi.file_name)
        )

        label_warning_of_the_order_of_axis = QtWidgets.QLabel()
        label_warning_of_the_order_of_axis.setText(
            '(' + self.translation.selected_language.get('any_choice_other_than',
                                                         'any choice other than 0 may lead to a shape mismatch, especially in 3D') + ')'
        )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        custom_growing_text_edit_for_name.setSizePolicy(sizePolicy)
        original_type_of_creation.setSizePolicy(sizePolicy)
        original_file_name.setSizePolicy(sizePolicy)
        label_warning_of_the_order_of_axis.setSizePolicy(sizePolicy)
        label_for_additional_info.setSizePolicy(sizePolicy)
        checkbox_visible.setSizePolicy(sizePolicy)
        label_table_name.setSizePolicy(sizePolicy)
        button_color.setSizePolicy(sizePolicy)

        qVBoxLayout = QtWidgets.QVBoxLayout()
        qHBoxLayout = QtWidgets.QHBoxLayout()

        combo_box = QComboBox()
        for each_type in self.list_of_choices:
            combo_box.addItem(each_type)

        combo_box.setCurrentIndex(
            self.dynamically_changeable_gi.index_of_users_choice_in_options_of_list_to_show)

        combo_box.activated[str].connect(self.set_type_of_plot)

        qVBoxLayout.addWidget(custom_growing_text_edit_for_name)
        qVBoxLayout.addWidget(original_type_of_creation)
        qVBoxLayout.addWidget(original_file_name)
        qVBoxLayout.addWidget(label_table_name)
        qVBoxLayout.addWidget(label_for_additional_info)
        qVBoxLayout.addWidget(checkbox_visible)
        qVBoxLayout.addWidget(label_warning_of_the_order_of_axis)
        qVBoxLayout.addWidget(combo_box)

        qHBoxLayout.addWidget(button_color, 0)
        qHBoxLayout.addLayout(qVBoxLayout, 1)

        frame_2 = QtWidgets.QFrame()
        frame_2.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Plain)
        frame_2.setLayout(qHBoxLayout)

        textLayout.addWidget(frame_2)
        textLayout.addWidget(frame)

    def set_type_of_plot(self, text):
        self.users_choice = text

    def set_list_of_lists_to_show(self):
        self.dynamically_changeable_gi.list_of_lists_of_values_to_show.clear()
        self.dynamically_changeable_gi.index_of_users_choice_in_options_of_list_to_show = \
            self.list_of_choices.index(self.users_choice)

        # choice 0 is: x:x, y:y, z:z
        if self.users_choice == self.list_of_choices[0]:
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[0])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[1])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[2])

        # choice 1 is: x:y, y:x, z:z
        if self.users_choice == self.list_of_choices[1]:
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[1])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[0])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[2])

        # choice 2 is: x:z, y:y, z:x
        if self.users_choice == self.list_of_choices[2]:
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[2])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[1])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[0])

        # choice 3 is: x:z, y:x, z:y
        if self.users_choice == self.list_of_choices[3]:
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[2])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[0])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[1])

        # choice 4 is: x:x, y:z, z:y
        if self.users_choice == self.list_of_choices[4]:
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[0])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[2])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[1])

        # choice 5 is: x:y, y:z, z:x
        if self.users_choice == self.list_of_choices[5]:
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[1])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[2])
            self.dynamically_changeable_gi.list_of_lists_of_values_to_show.append(
                self.dynamically_changeable_gi.final_list_of_x_y_z[0])

    def confirm_close_of_window(self):
        self.set_list_of_lists_to_show()
        self.parent.dynamically_changeable_gi = self.dynamically_changeable_gi
        self.reject()

    def closeEvent(self, event):
        '''
            Method to filter out closeEvent out of all events and to call confirm_close_of_window().
            Метод для фильтрации события из всех событий для корректного вызова 
            метода confirm_close_of_window().
        '''
        event.ignore()
        self.confirm_close_of_window()
