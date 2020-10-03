import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from datavisualizer.models.translation import *
from datavisualizer.models.connector import *
from datavisualizer.models.connection_object import *
from datavisualizer.models.custom_table_instance import *
from datavisualizer.models.graphics_instance import *
from datavisualizer.models.json_handler import *
from datavisualizer.models.pandas_model import *
from datavisualizer.models.project_instance_of_sql import *
from datavisualizer.models.project_instance import *

from datavisualizer.widgets.custom_widgets.gi_widget import *
from datavisualizer.widgets.custom_widgets.about_window import *
from datavisualizer.widgets.custom_widgets.custom_gi_dialog import *
from datavisualizer.widgets.custom_widgets.custom_sql_dialog import *
from datavisualizer.widgets.custom_widgets.global_info import *
from datavisualizer.widgets.custom_widgets.growing_text_edit import *
from datavisualizer.widgets.custom_widgets.help_window import *
from datavisualizer.widgets.custom_widgets.opening_window import *
from datavisualizer.widgets.custom_widgets.pi_widget import *
from datavisualizer.widgets.custom_widgets.table_subwindow import *
from datavisualizer.widgets.matplotlib_plots.custom_mpl import *
from datavisualizer.widgets.pyqtgraph_plots.custom_pyqtgraph import *


class DataVisualizer(QtWidgets.QMainWindow):
    """
        Class DataVisualizer сonnects GUI interaction with the models.
        Класс DataVisualizer соединяет взаимодействие представления с моделями.
    """

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.title = "DataVisualizer"
        self.setWindowTitle(self.title)
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas,
                            QtWidgets.QTabWidget.North)

        self.mdiArea = QMdiArea(self)
        self.setCentralWidget(self.mdiArea)
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.subWindowActivated.connect(
            self._deselect_all_subwindows_except_the_active_one)

        self.translation = Translation()
        self.connector = Connector()
        self.dynamically_changeable_gi = GraphicsInstance()
        self.list_of_sql_table_names = []

        # The limit is not that important. The higher the limit, the slower it gets to scroll mdiArea
        self.limit_of_opened_subwindows = 50
        self.list_of_subwindows = []
        self.docks_are_hidden = False

        self.help_window = HelpWindow()
        self.about_window = AboutWindow()

        self.showMaximized()

        self.set_plots_options_widget()
        self.set_graphics_menus_list_widget()
        self.set_projects_list_widget()

        self.mainMenu = QMenuBar(self)
        self.setMenuBar(self.mainMenu)

        menu_file = self.mainMenu.addMenu(
            self.translation.selected_language.get('file', 'File')
        )
        file_action_open_xls = menu_file.addAction(
            self.translation.selected_language.get(
                'open_excel_file', 'Open Excel file')
        )
        file_action_open_xls.triggered.connect(self.open_xls_file_dialog)

        file_action_open_csv = menu_file.addAction(
            self.translation.selected_language.get(
                'open_csv_file', 'Open CSV file')
        )
        file_action_open_csv.triggered.connect(self.open_csv_file_dialog)

        file_action_open_sql_object = menu_file.addAction(
            self.translation.selected_language.get(
                'open_sql_object', 'Open SQL object')
        )
        file_action_open_sql_object.triggered.connect(
            self.open_sql_object_dialog)

        menu_edit = self.mainMenu.addMenu(
            self.translation.selected_language.get('edit', 'Edit')
        )
        edit_action_export_as_png = menu_edit.addAction(
            self.translation.selected_language.get(
                'save_image_as', 'Save Image As...')
        )
        edit_action_export_as_png.triggered.connect(self.export_plot_as_png)

        menu_view = self.mainMenu.addMenu(
            self.translation.selected_language.get('view', 'View')
        )
        view_action_cascade = menu_view.addAction(
            self.translation.selected_language.get(
                'display_cascade', 'Display All Sub-windows As a Cascade')
        )
        view_action_cascade.triggered.connect(
            self.show_all_opened_sub_windows_as_a_cascade)

        view_action_tiled = menu_view.addAction(
            self.translation.selected_language.get(
                'display_optimally', 'Display All Sub-windows Optimally')
        )
        view_action_tiled.triggered.connect(self.show_all_opened_sub_windows)

        view_action_show_hide_docks = menu_view.addAction(
            self.translation.selected_language.get(
                'show_hide_docks', 'Show/Hide All Dock-Panels')
        )
        view_action_show_hide_docks.triggered.connect(self.show_hide_docks)

        menu_help = self.mainMenu.addMenu(
            self.translation.selected_language.get('help', 'Help')
        )
        help_action_show = menu_help.addAction(
            self.translation.selected_language.get('show_help', 'Show Help')
        )
        help_action_show.triggered.connect(self.show_help)

        menu_about = self.mainMenu.addMenu(
            self.translation.selected_language.get('about', 'About')
        )
        about_action_show = menu_about.addAction(
            self.translation.selected_language.get('show_about', 'Show About')
        )
        about_action_show.triggered.connect(self.show_about)
        self.mdiArea.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.Wheel and
                source is self.mdiArea.viewport()):
            return True
        return super(DataVisualizer, self).eventFilter(source, event)

    def export_plot_as_png(self):
        '''
            Method to export widget as PNG 
            Метод для экспорта элемента окна(виджета) 
            в качестве файла формата PNG
        '''
        try:
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            self.translation.selected_language.get(
                                                                'save_file', 'Save File'),
                                                            '.png', "Image (*.png *.jpg *.tif)")
            if name:
                img = self.mdiArea.grab()
                img.save(name)
        except:
            msg = GlobalInfo(
                self.translation.selected_language.get('failed_to_save',
                                                       'Failed to save the image: there is a problem with extension.')
            )

    def show_help(self):
        """
            Method to show external class: window with the help
            Метод для демонстрации внешнего класса: окна с инструкциями 
        """
        self.help_window.show()

    def show_about(self):
        """
            Method to show external class: window with information about program
            Метод для демонстрации внешнего класса: окна с информацией о программе и об авторе
        """
        self.about_window.show()

    def set_a_project(self, path, type_of_file, sql_table_name):
        project_instance = self._set_project_instance(
            path, type_of_file, sql_table_name)
        if not project_instance:
            raise
        for i, v in enumerate(project_instance.list_of_custom_table_instances):
            project_instance_widget = ProjectInstanceWidget()
            v.unique_id = self.connector.counter_of_custom_table_instances
            self.connector.counter_of_custom_table_instances += 1
            project_instance_widget.set_label_for_name(v.table_name)
            project_instance_widget.set_label_for_additional_info(v.file_name)
            v.path_to_icon = project_instance.path_to_icon
            project_instance_widget.set_label_for_icon(
                project_instance.path_to_icon)
            project_instance_item = QtWidgets.QListWidgetItem(
                self.projects_list_widget)
            project_instance_item.setSizeHint(
                project_instance_widget.sizeHint())
            self.projects_list_widget.addItem(project_instance_item)
            self.projects_list_widget.setItemWidget(
                project_instance_item, project_instance_widget)
            project_instance_widget.setContextMenuPolicy(
                QtCore.Qt.CustomContextMenu)
            project_instance_widget.customContextMenuRequested.connect(
                self.context_menu_of_project_instance_widget_clicked)

            win = TableSubWindow()
            win.setWindowTitle(v.table_name)
            win.setMinimumSize(QtCore.QSize(400, 400))
            win.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(1, 1)))
            self.mdiArea.addSubWindow(win)
            win.showMaximized()
            qvboxLayout = QVBoxLayout(win)
            qvboxLayout.setSpacing(1)
            qvboxLayout.setContentsMargins(2, 2, 2, 2)
            win.setLayout(qvboxLayout)

            v.sub_window = win
            v.table_view = QTableView(win)
            v.table_view.setModel(v.table_model)
            v.table_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            v.table_view.customContextMenuRequested.connect(
                self.context_menu_of_table_view_clicked)
            qvboxLayout.addWidget(v.table_view)
            self.connector.list_of_custom_table_instances.append(v)

    def _set_project_instance(self, path, type_of_file, sql_table_name):
        project_instance = None
        if (type_of_file == 'csv' or type_of_file == 'excel'):
            project_instance = ProjectInstance(path, type_of_file)
        else:
            project_instance = ProjectInstanceOfSqlObject(sql_table_name)
        return project_instance

    def _deselect_all_subwindows_except_the_active_one(self):
        for _, each_custom_table_instance in enumerate(
            self.connector.list_of_custom_table_instances
        ):
            if self.mdiArea.activeSubWindow():
                if not self.mdiArea.activeSubWindow().widget() is each_custom_table_instance.sub_window:
                    if not each_custom_table_instance.deleted:
                        each_custom_table_instance.table_view.clearSelection()

    def show_current_table(self):
        list_of_ids = [
            x.row() for x in self.projects_list_widget.selectedIndexes()
        ]
        list_of_valid_indexes = []
        for i, v in enumerate(self.connector.list_of_custom_table_instances):
            if not v.deleted:
                list_of_valid_indexes.append(i)
        for _, index in enumerate(list_of_ids):
            for i, v in enumerate(list_of_valid_indexes):
                if i is index:
                    self.connector.list_of_custom_table_instances[
                        v].sub_window.showMaximized()

    def set_graphics_instance(self, unique_id):
        for i, v in enumerate(self.connector.list_of_graphics_menus_instances):
            if not v.deleted:
                if v.unique_id is unique_id:
                    self._set_graphics_instance(unique_id)

    def _create_graphics_instance(self, users_choice_of_context_menu, table_id, table_name, file_name, list_of_cells):
        graphics_instance = GraphicsInstance()
        graphics_instance.table_id = table_id
        graphics_instance.table_name = table_name
        graphics_instance.file_name = file_name
        graphics_instance.name = \
            graphics_instance.set_name_of_graphical_instance(table_name)
        graphics_instance.index_of_users_choice_in_context_menu_of_creation_type = \
            users_choice_of_context_menu
        graphics_instance.list_of_cells = list_of_cells
        graphics_instance.list_of_x_y_z = \
            graphics_instance.set_values_by_users_choice(
                users_choice_of_context_menu, list_of_cells)
        if graphics_instance.list_of_x_y_z:
            return graphics_instance
        else:
            return None

    def create_graphics_instance(self, users_choice_of_context_menu, table_id, table_name, file_name, list_of_cells):
        graphics_instance = self._create_graphics_instance(
            users_choice_of_context_menu, table_id, table_name, file_name, list_of_cells
        )
        if not graphics_instance:
            msg = GlobalInfo(
                self.translation.selected_language.get(
                    'selected_cells_do_not_meet_req',
                    'Cluster of selected cells do not meet requirements of chosen action')
            )
            return
        graphics_instance.unique_id = self.connector.counter_of_graphics_instances
        self.connector.counter_of_graphics_instances += 1
        self.connector.list_of_graphics_menus_instances.append(
            graphics_instance)
        self.set_graphics_instance(graphics_instance.unique_id)

        graphics_instance_widget = GraphicsInstanceWidget()
        graphics_instance_widget.set_label_for_name(graphics_instance.name)
        graphics_instance_widget.set_label_for_additional_info(
            graphics_instance.original_type_of_creation)
        graphics_instance_widget.set_label_for_visibility(
            graphics_instance.visible)
        graphics_instance_widget.set_label_for_color(graphics_instance.color)
        graphics_instance_item = QtWidgets.QListWidgetItem(
            self.graphics_menus_list_widget)
        graphics_instance_item.setSizeHint(graphics_instance_widget.sizeHint())
        self.graphics_menus_list_widget.addItem(graphics_instance_item)
        self.graphics_menus_list_widget.setItemWidget(
            graphics_instance_item, graphics_instance_widget)
        graphics_instance_widget.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        graphics_instance_widget.customContextMenuRequested.connect(
            self.context_menu_of_graphics_instance_clicked)

    def set_projects_list_widget(self):
        self.projects_list_widget = QtWidgets.QListWidget(self)
        self.dock_widget_of_list_of_projects = QDockWidget(
            self.translation.selected_language.get('projects_list', 'Projects'), self)
        self.dock_widget_of_list_of_projects.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                                         QtWidgets.QDockWidget.DockWidgetMovable)
        self.projects_list_widget.itemDoubleClicked.connect(
            self.show_current_table)
        self.dock_widget_of_list_of_projects.setWidget(
            self.projects_list_widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                           self.dock_widget_of_list_of_projects)

    def set_graphics_menus_list_widget(self):
        self.graphics_menus_list_widget = QtWidgets.QListWidget(self)
        self.dock_widget_of_list_of_graphics_menus = QDockWidget(
            self.translation.selected_language.get('graphics_menus', 'Graphics Menus'), self)
        self.dock_widget_of_list_of_graphics_menus.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                                               QtWidgets.QDockWidget.DockWidgetMovable)
        self.dock_widget_of_list_of_graphics_menus.setWidget(
            self.graphics_menus_list_widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                           self.dock_widget_of_list_of_graphics_menus)

    def set_type_of_plot(self, text):
        self.connector.type_of_plot = text

    def _set_dict_for_the_next_plot(self):
        dict_of_chosen_options_for_current_plot = {
            'show_legend': self.connector.show_legend,
            'show_axis_names': self.connector.show_axis_names,
            'name_of_axis_x': self.connector.name_of_axis_x,
            'name_of_axis_y': self.connector.name_of_axis_y,
            'name_of_axis_z': self.connector.name_of_axis_z,
        }
        return dict_of_chosen_options_for_current_plot

    def _create_subwindow_by_type_of_plot(self):

        if (self.connector.type_of_plot == self.connector.dict_of_plot_types['===== 2D: simple and fast: =====']
            or self.connector.type_of_plot == self.connector.dict_of_plot_types['===== 2D: pyqtgraph (advanced): =====']
            or self.connector.type_of_plot == self.connector.dict_of_plot_types['===== 3D: 1st type =====']
                or self.connector.type_of_plot == self.connector.dict_of_plot_types['===== 3D: 2nd type =====']):
            msg = GlobalInfo(
                self.translation.selected_language.get(
                    'msg_have_not_chosen_any_plot', 'You have not chosen the type of plot')
            )
            return

        dict_of_chosen_options_for_current_plot = self._set_dict_for_the_next_plot()
        win = None

        if self.connector.type_of_plot == self.connector.dict_of_plot_types['2D plot (matplotlib)']:
            win = MPL2DPlot(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['2D plot (pyqtgraph)']:
            win = PyqtgraphSimplePlot(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['2D interactive plot (pyqtgraph)']:
            win = PyqtgraphAdvancedPlot(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['2D double plot (pyqtgraph)']:
            win = PyqtgraphDoublePlot(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['2D linked plots by axis X (pyqtgraph)']:
            win = PyqtgraphLinkedXPlot(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['2D linked plots by axis Y (pyqtgraph)']:
            win = PyqtgraphLinkedYPlot(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['3D scatter plot 1st type (matplotlib)']:
            win = MPLScatterFirstType(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['3D wireframe plot 1st type (matplotlib)']:
            win = MPLWireframeFirstType(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['3D surface plot 1st type (matplotlib)']:
            win = MPLSurfaceFirstType(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['3D scatter plot 2nd type (matplotlib)']:
            win = MPLScatterSecondType(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['3D wireframe plot 2nd type (matplotlib)']:
            win = MPLWireframeSecondType(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if self.connector.type_of_plot == self.connector.dict_of_plot_types['3D surface plot 2nd type (matplotlib)']:
            win = MPLSurfaceSecondType(
                self.connector.list_of_graphics_menus_instances,
                dict_of_chosen_options_for_current_plot)
        if win:
            win.setWindowTitle(self.connector.type_of_plot)
            win.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(1, 1)))
            win.setMinimumSize(QtCore.QSize(400, 400))
            self.list_of_subwindows.append(win)
            self.mdiArea.addSubWindow(win)
            win.showMaximized()

    def create_plot_subwindow(self):
        if self.connector.delete_previous_plots:
            self.mdiArea.closeAllSubWindows()
            for i, v in enumerate(self.connector.list_of_custom_table_instances):
                if not v.deleted:
                    v.sub_window.showMaximized()
            self.mdiArea.tileSubWindows()
        if len(self.mdiArea.subWindowList()) < self.limit_of_opened_subwindows:
            self._create_subwindow_by_type_of_plot()
        else:
            msg = GlobalInfo(
                self.translation.selected_language.get(
                    'limit_reached',
                    'The limit for open sub-windows reached. Close subwindows which you may not need.')
            )
        if self.connector.display_previous_subwindows:
            self.mdiArea.tileSubWindows()

    def show_all_opened_sub_windows_as_a_cascade(self):
        self.mdiArea.cascadeSubWindows()

    def show_all_opened_sub_windows(self):
        self.mdiArea.tileSubWindows()

    def update_all_docks(self):
        self.dock_widget_of_list_of_graphics_menus.update()
        self.dock_widget_of_list_of_projects.update()
        self.dock_widget_of_plots_options.update()

    def show_hide_docks(self):
        self.update_all_docks()
        if self.docks_are_hidden:
            self.dock_widget_of_list_of_graphics_menus.setHidden(False)
            self.dock_widget_of_list_of_projects.setHidden(False)
            self.dock_widget_of_plots_options.setHidden(False)
            self.docks_are_hidden = False
            self.update_all_docks()
            return
        else:
            self.dock_widget_of_list_of_graphics_menus.setHidden(True)
            self.dock_widget_of_list_of_projects.setHidden(True)
            self.dock_widget_of_plots_options.setHidden(True)
            self.docks_are_hidden = True
            self.update_all_docks()
            return

    def open_xls_file_dialog(self):
        '''
            Method to open only Excel Files (*.xls *.xlsx *.xlsm)
            Метод для открытия только файлов Excel форматов xls, xlsx, xlsm
        '''
        try:
            path, _ = QFileDialog.getOpenFileName(self,
                                                  self.translation.selected_language.get(
                                                      'open_file', 'Open File'),
                                                  "*.xls, *.xlsx, *.xlsm",
                                                  "Excel Files (*.xls *.xlsx *.xlsm)",
                                                  options=QFileDialog.DontUseNativeDialog)
            if (path):
                self.set_a_project(path, 'excel', None)
        except:
            pass

    def open_sql_object_dialog(self):
        try:
            connection_object = ConnectionObject()
            self.list_of_sql_table_names = connection_object.get_list_of_tables()
            if self.list_of_sql_table_names:
                custom_sql_dialog = CustomSqlDialog(self)
                custom_sql_dialog.exec_()
                if (self.selected_sql_table):
                    self.set_a_project(None, None, self.selected_sql_table)
                self.list_of_sql_table_names = None
                self.selected_sql_table = None
            connection_object.connection.close()
        except:
            msg = GlobalInfo(
                self.translation.selected_language.get(
                    'msg_could_not_create_a_connection', 'Could not create a connection. Please, check the file called config_sql.json')
            )

    def open_csv_file_dialog(self):
        '''
            Method to open only CSV Files (*.csv)
            Метод для открытия только файлов CSV
        '''
        try:
            path, _ = QFileDialog.getOpenFileName(self,
                                                  self.translation.selected_language.get(
                                                      'open_file', 'Open File'),
                                                  "*.csv",
                                                  "CSV Files (*.csv)",
                                                  options=QFileDialog.DontUseNativeDialog)
            if (path):
                self.set_a_project(path, 'csv', None)
        except:
            pass

    def _get_selected_cells(self, list_of_selected_cells):
        '''
            Method returns boundary values of cells (selected by user).
            Метод возвращает граничные значения выделенных пользователем ячеек.
        '''
        list_of_lists_of_column_with_row_of_selected_cells = []
        for index, each_selected_cell in enumerate(list_of_selected_cells):
            list_of_lists_of_column_with_row_of_selected_cells.append(
                [each_selected_cell.column(), each_selected_cell.row()]
            )
        return list_of_lists_of_column_with_row_of_selected_cells

    def context_menu_of_table_view_clicked(self, position):
        '''
            Method to call a context menu for different actions.
            Метод для вызова контекстного меню с различными действиями.
        '''
        for i, v in enumerate(self.connector.list_of_custom_table_instances):
            if not v.deleted:
                if v.table_view.selectionModel().selection().indexes():

                    menu = QtWidgets.QMenu()

                    sub_menu_2d = QMenu(menu)
                    sub_menu_2d.setTitle(
                        self.translation.selected_language.get(
                            'creation_of_2d', '2D Creation')
                    )

                    sub_sub_menu_2d_rows = QMenu(sub_menu_2d)
                    sub_sub_menu_2d_rows.setTitle(
                        self.translation.selected_language.get(
                            'connect_selected_values_as_clusters_of_rows', 'Connect selected values as clusters of rows')
                    )

                    sub_sub_menu_2d_columns = QMenu(sub_menu_2d)
                    sub_sub_menu_2d_columns.setTitle(
                        self.translation.selected_language.get(
                            'connect_selected_values_as_clusters_of_columns', 'Connect selected values as clusters of columns')
                    )

                    sub_menu_3d = QMenu(menu)
                    sub_menu_3d.setTitle(
                        self.translation.selected_language.get(
                            'creation_of_3d', '3D creation')
                    )

                    sub_sub_menu_3d_1st_type = QMenu(sub_menu_3d)
                    sub_sub_menu_3d_1st_type.setTitle(
                        self.translation.selected_language.get(
                            'first_type', '1st type') + ': ' +
                        self.translation.selected_language.get(
                            'selected_cells_determine_shape_of_a_matrix',
                            'Selected cells determine a matrix [m x n] (m - columns, n - rows)')
                    )

                    sub_sub_menu_3d_2nd_type = QMenu(sub_menu_3d)
                    sub_sub_menu_3d_2nd_type.setTitle(
                        self.translation.selected_language.get(
                            'second_type', '2nd type') + ': ' +
                        self.translation.selected_language.get(
                            'selected_cells_are_3_rows_or_3_columns',
                            'Selected cells are 3 rows or 3 columns')
                    )

                    set_as_clusters_of_rows_value_as_Y_column_index_as_X = sub_sub_menu_2d_rows.addAction(
                        self.translation.selected_language.get(
                            'set_as_clusters_of_rows_value_as_y_column_index_as_x', 'Set as clusters of rows: value as Y, column index as X')
                    )
                    set_as_clusters_of_rows_1st_row_values_as_X_2nd_row_values_as_Y = sub_sub_menu_2d_rows.addAction(
                        self.translation.selected_language.get(
                            'set_as_clusters_of_rows_1st_row_values_as_x_2nd_row_values_as_y', 'Set as clusters of rows: 1st row values as X, 2nd row values as Y')
                    )
                    set_as_clusters_of_columns_value_as_Y_row_index_as_X = sub_sub_menu_2d_columns.addAction(
                        self.translation.selected_language.get(
                            'set_as_clusters_of_columns_value_as_y_row_index_as_x', 'Set as clusters of columns: value as Y, row index as X')
                    )
                    set_as_clusters_of_columns_1st_column_values_as_X_2nd_column_values_as_Y = sub_sub_menu_2d_columns.addAction(
                        self.translation.selected_language.get(
                            'set_as_clusters_of_columns_1st_column_values_as_x_2nd_column_values_as_y', 'Set as clusters of columns: 1st column values as X, 2nd column values as Y')
                    )

                    sub_menu_2d.addMenu(sub_sub_menu_2d_rows)
                    sub_menu_2d.addMenu(sub_sub_menu_2d_columns)

                    set_selected_values_as_Z_numbers_of_columns_as_X_numbers_of_rows_as_Y = sub_sub_menu_3d_1st_type.addAction(
                        self.translation.selected_language.get(
                            'set_selected_values_as_z_numbers_of_columns_as_x_numbers_of_rows_as_y', 'Set selected values as Z, numbers of columns as X, numbers of rows as Y')
                    )

                    set_selected_values_as_Z_numbers_from_1_to_n_as_X_numbers_from_1_to_m_as_Y = sub_sub_menu_3d_1st_type.addAction(
                        self.translation.selected_language.get('set_selected_values_as_z_numbers_from_1_to_n_as_x_numbers_from_1_to_m_as_y',
                                                               'Set selected values as Z, numbers from 1 to n as X, numbers from 1 to m as Y')
                    )

                    set_as_clusters_of_rows_1st_row_values_as_X_2nd_row_values_as_Y_3rd_row_values_as_Z = sub_sub_menu_3d_2nd_type.addAction(
                        self.translation.selected_language.get('set_as_clusters_of_rows_1st_row_values_as_x_2nd_row_values_as_y_3rd_row_values_as_z',
                                                               'Set as clusters of rows, 1st row values as X, 2nd row values as Y, 3rd row values as Z')
                    )
                    set_as_clusters_of_columns_1st_column_values_as_X_2nd_column_values_as_Y_3rd_column_values_as_Z = sub_sub_menu_3d_2nd_type.addAction(
                        self.translation.selected_language.get('set_as_clusters_of_columns_1st_column_values_as_x_2nd_column_values_as_y_3rd_column_values_as_z',
                                                               'Set as clusters of columns, 1st column values as X, 2nd column values as Y, 3rd column values as Z')
                    )

                    sub_menu_3d.addMenu(sub_sub_menu_3d_1st_type)
                    sub_menu_3d.addMenu(sub_sub_menu_3d_2nd_type)

                    menu.addMenu(sub_menu_2d)
                    menu.addMenu(sub_menu_3d)
                    action = menu.exec_(v.table_view.mapToGlobal(position))
                    if action == set_as_clusters_of_rows_value_as_Y_column_index_as_X:
                        list_of_cells = self._get_selected_cells(
                            v.table_view.selectedIndexes())
                        self.create_graphics_instance(  # 21 means 2d, 1st users choice
                            21, v.unique_id, v.table_name, v.file_name, list_of_cells
                        )
                    if action == set_as_clusters_of_rows_1st_row_values_as_X_2nd_row_values_as_Y:
                        list_of_cells = self._get_selected_cells(
                            v.table_view.selectedIndexes())
                        self.create_graphics_instance(  # 22 means 2d, 2nd users choice
                            22, v.unique_id, v.table_name, v.file_name, list_of_cells
                        )
                    if action == set_as_clusters_of_columns_value_as_Y_row_index_as_X:
                        list_of_cells = self._get_selected_cells(
                            v.table_view.selectedIndexes())
                        self.create_graphics_instance(  # 23 means 2d, 3rd users choice
                            23, v.unique_id, v.table_name, v.file_name, list_of_cells
                        )
                    if action == set_as_clusters_of_columns_1st_column_values_as_X_2nd_column_values_as_Y:
                        list_of_cells = self._get_selected_cells(
                            v.table_view.selectedIndexes())
                        self.create_graphics_instance(  # 24 means 2d, 4th users choice
                            24, v.unique_id, v.table_name, v.file_name, list_of_cells
                        )
                    if action == set_selected_values_as_Z_numbers_of_columns_as_X_numbers_of_rows_as_Y:
                        list_of_cells = self._get_selected_cells(
                            v.table_view.selectedIndexes())
                        self.create_graphics_instance(  # 31 means 3d, 1st users choice
                            31, v.unique_id, v.table_name, v.file_name, list_of_cells
                        )
                    if action == set_selected_values_as_Z_numbers_from_1_to_n_as_X_numbers_from_1_to_m_as_Y:
                        list_of_cells = self._get_selected_cells(
                            v.table_view.selectedIndexes())
                        self.create_graphics_instance(  # 32 means 3d, 2nd users choice
                            32, v.unique_id, v.table_name, v.file_name, list_of_cells
                        )
                    if action == set_as_clusters_of_rows_1st_row_values_as_X_2nd_row_values_as_Y_3rd_row_values_as_Z:
                        list_of_cells = self._get_selected_cells(
                            v.table_view.selectedIndexes())
                        self.create_graphics_instance(  # 33 means 3d, 3rd users choice
                            33, v.unique_id, v.table_name, v.file_name, list_of_cells
                        )
                    if action == set_as_clusters_of_columns_1st_column_values_as_X_2nd_column_values_as_Y_3rd_column_values_as_Z:
                        list_of_cells = self._get_selected_cells(
                            v.table_view.selectedIndexes())
                        self.create_graphics_instance(  # 34 means 3d, 4th users choice
                            34, v.unique_id, v.table_name, v.file_name, list_of_cells
                        )

    def _filter_type_of_value(self, value, graphics_instance):
        if type(value) is not float:
            try:
                return float(value)
            except:
                graphics_instance.contains_non_original_zero_values = True
                return 0
        return value

    def _set_graphics_instance(self, unique_id):
        gi = self.connector.list_of_graphics_menus_instances[unique_id]
        if gi.list_of_x_y_z:
            if not gi.list_of_x_y_z[0]:
                for i, v in enumerate(gi.list_of_x_to_load):
                    _list = []
                    for _, each_row in enumerate(v):
                        _list.append(
                            self._filter_type_of_value(self.connector.list_of_custom_table_instances[
                                gi.table_id].table_model._data.iloc[each_row[1], each_row[0]], gi)
                        )
                    gi.list_of_x_y_z[0].append(_list)
            if not gi.list_of_x_y_z[1]:
                for i, v in enumerate(gi.list_of_y_to_load):
                    _list = []
                    for _, each_row in enumerate(v):
                        _list.append(
                            self._filter_type_of_value(self.connector.list_of_custom_table_instances[
                                gi.table_id].table_model._data.iloc[each_row[1], each_row[0]], gi)
                        )
                    gi.list_of_x_y_z[1].append(_list)
            if not gi.list_of_x_y_z[2]:
                for i, v in enumerate(gi.list_of_z_to_load):
                    _list = []
                    for _, each_row in enumerate(v):
                        _list.append(
                            self._filter_type_of_value(self.connector.list_of_custom_table_instances[
                                gi.table_id].table_model._data.iloc[each_row[1], each_row[0]], gi)
                        )
                    gi.list_of_x_y_z[2].append(_list)
        self.connector.list_of_graphics_menus_instances[unique_id].color = \
            self.connector.list_of_graphics_menus_instances[unique_id].randomize_color(
        )
        self.connector.list_of_graphics_menus_instances[unique_id].final_list_of_x_y_z = [
            gi.list_of_x_y_z[0],
            gi.list_of_x_y_z[1],
            gi.list_of_x_y_z[2],
        ]
        self.connector.list_of_graphics_menus_instances[unique_id].list_of_lists_of_values_to_show = [
            gi.list_of_x_y_z[0],
            gi.list_of_x_y_z[1],
            gi.list_of_x_y_z[2],
        ]
        self.connector.list_of_graphics_menus_instances[
            unique_id].set_number_of_values_of_each_axis()
        if gi.contains_non_original_zero_values:
            msg = GlobalInfo(
                self.translation.selected_language.get(
                    'converted_to_zero', 'All non-integer/non-float values have been converted to 0')
            )

    def context_menu_of_graphics_instance_clicked(self, position):
        menu = QtWidgets.QMenu()
        options_action = menu.addAction(
            self.translation.selected_language.get('options', 'Options')
        )
        create_a_copy_action = menu.addAction(
            self.translation.selected_language.get(
                'create_copy', 'Create a copy')
        )
        change_visible_state = menu.addAction(
            self.translation.selected_language.get('show_hide', 'Show/Hide')
        )
        delete_action = menu.addAction(
            self.translation.selected_language.get('delete', 'Delete')
        )
        action = menu.exec_(self.sender().mapToGlobal(position))

        if action == change_visible_state:
            list_of_ids = [
                x.row() for x in self.graphics_menus_list_widget.selectedIndexes()
            ]
            list_of_valid_indexes = []
            for i, v in enumerate(self.connector.list_of_graphics_menus_instances):
                if not v.deleted and not v.table_deleted:
                    list_of_valid_indexes.append(i)
            for _, index in enumerate(list_of_ids):
                for i, v in enumerate(list_of_valid_indexes):
                    if i is index:
                        if self.connector.list_of_graphics_menus_instances[v].visible:
                            self.connector.list_of_graphics_menus_instances[
                                v].visible = False
                        else:
                            self.connector.list_of_graphics_menus_instances[
                                v].visible = True

        if action == create_a_copy_action:
            list_of_ids = [
                x.row() for x in self.graphics_menus_list_widget.selectedIndexes()
            ]
            list_of_valid_indexes = []
            for i, v in enumerate(self.connector.list_of_graphics_menus_instances):
                if not v.deleted and not v.table_deleted:
                    list_of_valid_indexes.append(i)
            for _, index in enumerate(list_of_ids):
                for i, v in enumerate(list_of_valid_indexes):
                    if i is index:
                        self.create_graphics_instance(
                            self.connector.list_of_graphics_menus_instances[
                                v].index_of_users_choice_in_context_menu_of_creation_type,
                            self.connector.list_of_graphics_menus_instances[v].table_id,
                            self.connector.list_of_graphics_menus_instances[v].table_name,
                            self.connector.list_of_graphics_menus_instances[v].file_name,
                            self.connector.list_of_graphics_menus_instances[v].list_of_cells
                        )

        if action == options_action:
            list_of_ids = [
                x.row() for x in self.graphics_menus_list_widget.selectedIndexes()
            ]
            list_of_valid_indexes = []
            for i, v in enumerate(self.connector.list_of_graphics_menus_instances):
                if not v.deleted and not v.table_deleted:
                    list_of_valid_indexes.append(i)
            for _, index in enumerate(list_of_ids):
                for i, v in enumerate(list_of_valid_indexes):
                    if i is index:
                        self.dynamically_changeable_gi = \
                            self.connector.list_of_graphics_menus_instances[v]
                        self.customDialogOfGraphicsInstance = CustomDialogOfGraphicsInstance(
                            self)
                        self.customDialogOfGraphicsInstance.exec_()
                        self.connector.list_of_graphics_menus_instances[v] = \
                            self.dynamically_changeable_gi
                        self.dynamically_changeable_gi = None

        if action == delete_action:
            if self.confirm_deletion_of_selected_item('graphics_instance'):
                list_of_ids = [
                    x.row() for x in self.graphics_menus_list_widget.selectedIndexes()
                ]
                list_of_valid_indexes = []
                for i, v in enumerate(self.connector.list_of_graphics_menus_instances):
                    if not v.deleted and not v.table_deleted:
                        list_of_valid_indexes.append(i)
                for _, index in enumerate(list_of_ids):
                    for i, v in enumerate(list_of_valid_indexes):
                        if i is index:
                            self.connector.list_of_graphics_menus_instances[
                                v].deleted = True
        self.update_graphics_menus_list_widget()

    def update_graphics_menus_list_widget(self):
        '''
            Method to update graphs of QListWidget.
            Метод для обновления графиков элемента QListWidget.
        '''
        self.graphics_menus_list_widget.clear()
        for i, table in enumerate(self.connector.list_of_custom_table_instances):
            for _, v in enumerate(self.connector.list_of_graphics_menus_instances):
                if v.table_id is table.unique_id:
                    if table.deleted:
                        v.table_deleted = True
        for i, v in enumerate(self.connector.list_of_graphics_menus_instances):
            if not v.deleted and not v.table_deleted:
                graphics_instance_widget = GraphicsInstanceWidget()
                graphics_instance_widget.set_label_for_name(v.name)
                graphics_instance_widget.set_label_for_additional_info(
                    v.original_type_of_creation)
                graphics_instance_widget.set_label_for_visibility(v.visible)
                graphics_instance_widget.set_label_for_color(v.color)
                graphics_instance_item = QtWidgets.QListWidgetItem(
                    self.graphics_menus_list_widget)
                graphics_instance_item.setSizeHint(
                    graphics_instance_widget.sizeHint())
                self.graphics_menus_list_widget.addItem(graphics_instance_item)
                self.graphics_menus_list_widget.setItemWidget(
                    graphics_instance_item, graphics_instance_widget)
                graphics_instance_widget.setContextMenuPolicy(
                    QtCore.Qt.CustomContextMenu)
                graphics_instance_widget.customContextMenuRequested.connect(
                    self.context_menu_of_graphics_instance_clicked)

    def update_projects_list_widget(self):
        '''
            Method to update graphs of QListWidget.
            Метод для обновления графиков элемента QListWidget.
        '''
        self.projects_list_widget.clear()
        for i, v in enumerate(self.connector.list_of_custom_table_instances):
            if not v.deleted:
                project_instance_widget = ProjectInstanceWidget()
                project_instance_widget.set_label_for_name(v.table_name)
                project_instance_widget.set_label_for_additional_info(
                    v.file_name)
                project_instance_widget.set_label_for_icon(v.path_to_icon)
                project_instance_item = QtWidgets.QListWidgetItem(
                    self.projects_list_widget)
                project_instance_item.setSizeHint(
                    project_instance_widget.sizeHint())
                self.projects_list_widget.addItem(project_instance_item)
                self.projects_list_widget.setItemWidget(
                    project_instance_item, project_instance_widget)
                project_instance_widget.setContextMenuPolicy(
                    QtCore.Qt.CustomContextMenu)
                project_instance_widget.customContextMenuRequested.connect(
                    self.context_menu_of_project_instance_widget_clicked)
        self.update_graphics_menus_list_widget()

    def context_menu_of_project_instance_widget_clicked(self, position):
        menu = QtWidgets.QMenu()
        delete_action = menu.addAction(
            self.translation.selected_language.get('delete', 'Delete')
        )
        action = menu.exec_(self.sender().mapToGlobal(position))
        if action == delete_action:
            list_of_ids = [
                x.row() for x in self.projects_list_widget.selectedIndexes()
            ]
            list_of_valid_indexes = []
            for i, v in enumerate(self.connector.list_of_custom_table_instances):
                if not v.deleted:
                    list_of_valid_indexes.append(i)
            for _, index in enumerate(list_of_ids):
                for i, v in enumerate(list_of_valid_indexes):
                    if i is index:
                        self.connector.list_of_custom_table_instances[
                            v].deleted = True
                        self.connector.list_of_custom_table_instances[
                            v].sub_window._want_to_close = True
            if self.confirm_deletion_of_selected_item('project_instance'):
                self.mdiArea.closeAllSubWindows()
                for i, v in enumerate(self.connector.list_of_custom_table_instances):
                    if not v.deleted:
                        v.sub_window.showMaximized()
                self.mdiArea.tileSubWindows()
                self.update_projects_list_widget()

    def set_plots_options_widget(self):
        self.dock_widget_of_plots_options = QDockWidget(
            self.translation.selected_language.get('options', 'Options'),
            self)
        self.dock_widget_of_plots_options.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                                      QtWidgets.QDockWidget.DockWidgetMovable)

        widget_options = QWidget(self.dock_widget_of_plots_options)
        qvboxLayout = QVBoxLayout(widget_options)
        qvboxLayout.setSpacing(1)
        qvboxLayout.setContentsMargins(2, 2, 2, 2)
        widget_options.setLayout(qvboxLayout)

        def update_clicked(arg):
            self.create_plot_subwindow()

        button_update_the_graph = QPushButton()
        button_update_the_graph.setText(
            self.translation.selected_language.get(
                'create_new_plot', 'Create a new plot')
        )
        button_update_the_graph.setStyleSheet(
            'QPushButton {background-color:rgb(170, 255, 0); color: black;}')
        button_update_the_graph.clicked.connect(update_clicked)

        def checkbox_for_previous_plots_deletion_clicked(arg):
            if checkbox_for_previous_plots_deletion.isChecked():
                self.connector.delete_previous_plots = True
            else:
                self.connector.delete_previous_plots = False

        checkbox_for_previous_plots_deletion = QCheckBox()
        checkbox_for_previous_plots_deletion.setText(
            self.translation.selected_language.get(
                'delete_previous_plots', 'Delete previous plots')
        )
        checkbox_for_previous_plots_deletion.setChecked(True)
        checkbox_for_previous_plots_deletion.toggled.connect(
            checkbox_for_previous_plots_deletion_clicked)

        def checkbox_for_displaying_previous_subwindows_clicked(arg):
            if checkbox_for_displaying_previous_subwindows.isChecked():
                self.connector.display_previous_subwindows = True
            else:
                self.connector.display_previous_subwindows = False

        checkbox_for_displaying_previous_subwindows = QCheckBox()
        checkbox_for_displaying_previous_subwindows.setText(
            self.translation.selected_language.get(
                'display_previous_subwindows', 'Display previous sub-windows')
        )
        checkbox_for_displaying_previous_subwindows.setChecked(True)
        checkbox_for_displaying_previous_subwindows.toggled.connect(
            checkbox_for_displaying_previous_subwindows_clicked)

        combo_box = QComboBox()
        for each_type in self.connector.list_of_plot_types:
            combo_box.addItem(each_type)

        combo_box.activated[str].connect(self.set_type_of_plot)

        label_axis_x_y_z = QtWidgets.QLabel()
        label_axis_x_y_z.setText(
            self.translation.selected_language.get(
                'names_of_axis_x_y_z', 'Names of axis X, Y, Z') + ": "
        )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        text_edit_axis_x = GrowingTextEdit()
        text_edit_axis_x.setSizePolicy(sizePolicy)
        text_edit_axis_x.setMinimumHeight(27)
        text_edit_axis_x.setMaximumHeight(27)
        text_edit_axis_x.setText(
            str(self.connector.name_of_axis_x)
        )

        def text_edit_axis_x_changed():
            try:
                self.connector.name_of_axis_x = text_edit_axis_x.toPlainText()
            except:
                self.connector.name_of_axis_x = 'Incorrect symbols in name'

        text_edit_axis_x.textChanged.connect(text_edit_axis_x_changed)

        text_edit_axis_y = GrowingTextEdit()
        text_edit_axis_y.setSizePolicy(sizePolicy)
        text_edit_axis_y.setMinimumHeight(27)
        text_edit_axis_y.setMaximumHeight(27)
        text_edit_axis_y.setText(
            str(self.connector.name_of_axis_y)
        )

        def text_edit_axis_y_changed():
            try:
                self.connector.name_of_axis_y = text_edit_axis_y.toPlainText()
            except:
                self.connector.name_of_axis_y = 'Incorrect symbols in name'

        text_edit_axis_y.textChanged.connect(text_edit_axis_y_changed)

        text_edit_axis_z = GrowingTextEdit()
        text_edit_axis_z.setSizePolicy(sizePolicy)
        text_edit_axis_z.setMinimumHeight(27)
        text_edit_axis_z.setMaximumHeight(27)
        text_edit_axis_z.setText(
            str(self.connector.name_of_axis_z)
        )

        def text_edit_axis_z_changed():
            try:
                self.connector.name_of_axis_z = text_edit_axis_z.toPlainText()
            except:
                self.connector.name_of_axis_z = 'Incorrect symbols in name'

        text_edit_axis_z.textChanged.connect(text_edit_axis_z_changed)

        def checkbox_for_legend_clicked(arg):
            if checkbox_for_legend.isChecked():
                self.connector.show_legend = True
            else:
                self.connector.show_legend = False

        checkbox_for_legend = QCheckBox()
        checkbox_for_legend.setText(
            self.translation.selected_language.get(
                'show_legend', 'Show legend')
        )
        checkbox_for_legend.setChecked(True)
        checkbox_for_legend.toggled.connect(
            checkbox_for_legend_clicked)

        def checkbox_for_axis_names_clicked(arg):
            if checkbox_for_axis_names.isChecked():
                self.connector.show_axis_names = True
            else:
                self.connector.show_axis_names = False

        checkbox_for_axis_names = QCheckBox()
        checkbox_for_axis_names.setText(
            self.translation.selected_language.get(
                'show_axis_names', 'Show axis names')
        )
        checkbox_for_axis_names.setChecked(True)
        checkbox_for_axis_names.toggled.connect(
            checkbox_for_axis_names_clicked)

        qvboxLayout.addWidget(button_update_the_graph)
        qvboxLayout.addWidget(combo_box)
        qvboxLayout.addWidget(checkbox_for_previous_plots_deletion)
        qvboxLayout.addWidget(checkbox_for_displaying_previous_subwindows)
        qvboxLayout.addWidget(checkbox_for_legend)
        qvboxLayout.addWidget(checkbox_for_axis_names)
        qvboxLayout.addWidget(label_axis_x_y_z)
        qvboxLayout.addWidget(text_edit_axis_x)
        qvboxLayout.addWidget(text_edit_axis_y)
        qvboxLayout.addWidget(text_edit_axis_z)

        qvboxLayout.addItem(QtWidgets.QSpacerItem(
            10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        self.dock_widget_of_plots_options.setWidget(widget_options)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.dock_widget_of_plots_options)

    def confirm_deletion_of_selected_item(self, type_of_selected_item_as_str):
        msg = QMessageBox()
        msg.setWindowTitle(
            self.translation.selected_language.get(
                'confirm_deletion', 'Confirm deletion')
        )
        if type_of_selected_item_as_str == 'graphics_instance':
            msg.setText(
                self.translation.selected_language.get(
                    'want_to_delete_selected_item', 'Are you sure you want to delete selected item?')
            )
        if type_of_selected_item_as_str == 'project_instance':
            msg.setText(
                str(self.translation.selected_language.get(
                    'want_to_delete_selected_item', 'Are you sure you want to delete selected item?'))
                + '\n' +
                self.translation.selected_language.get(
                    'all_subwindows_will_close', 'If you delete selected table, all sub-windows will close.')
            )
        okButton = msg.addButton(
            self.translation.selected_language.get('yes', 'Yes'),
            QMessageBox.AcceptRole
        )
        msg.addButton(
            self.translation.selected_language.get('no', 'No'),
            QMessageBox.RejectRole
        )
        msg.exec()
        if msg.clickedButton() == okButton:
            return True
        return False

    def confirm_close_of_application(self):
        '''
            Method to safely close the application only with the confirmation of the user.
            Метод для безопасного закрытия приложения с подтверждением выхода.
        '''
        msg = QMessageBox()
        msg.setWindowTitle(
            self.translation.selected_language.get(
                'confirm_exit', 'Confirm exit')
        )
        msg.setText(
            self.translation.selected_language.get(
                'want_to_exit', 'Are you sure you want to exit?')
        )
        okButton = msg.addButton(
            self.translation.selected_language.get('yes', 'Yes'),
            QMessageBox.AcceptRole
        )
        msg.addButton(
            self.translation.selected_language.get('no', 'No'),
            QMessageBox.RejectRole
        )
        msg.exec()
        if msg.clickedButton() == okButton:
            sys.exit()

    def closeEvent(self, event):
        '''
            Method to filter out closeEvent out of all events and to call confirm_close_of_application().
            Метод для фильтрации события из всех событий для корректного вызова 
            метода confirm_close_of_application().
        '''
        event.ignore()
        self.confirm_close_of_application()
