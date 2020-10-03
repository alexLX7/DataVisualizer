import datavisualizer.models.translation as translation


class Connector:
    '''
        Class to set and connect different pieces of view and models
        Класс для инициализации и взаимодействия различных элементов интерфейса и моделей
    '''

    def __init__(self):
        self.translation = translation.Translation()
        self.list_of_custom_table_instances = []
        self.counter_of_custom_table_instances = 0
        self.list_of_graphics_menus_instances = []
        self.counter_of_graphics_instances = 0
        self.dict_of_plot_types = {}
        self.list_of_plot_types = [
            '===== 2D: simple and fast: =====',
            '2D plot (matplotlib)',
            '2D plot (pyqtgraph)',
            '===== 2D: pyqtgraph (advanced): =====',
            '2D interactive plot (pyqtgraph)',
            '2D double plot (pyqtgraph)',
            '2D linked plots by axis X (pyqtgraph)',
            '2D linked plots by axis Y (pyqtgraph)',
            '===== 3D: 1st type =====',
            '3D scatter plot 1st type (matplotlib)',
            '3D wireframe plot 1st type (matplotlib)',
            '3D surface plot 1st type (matplotlib)',
            '===== 3D: 2nd type =====',
            '3D scatter plot 2nd type (matplotlib)',
            '3D wireframe plot 2nd type (matplotlib)',
            '3D surface plot 2nd type (matplotlib)',
        ]
        for i, v in enumerate(self.list_of_plot_types):
            self.dict_of_plot_types[v] = v
        self.type_of_plot = self.list_of_plot_types[0]
        self.delete_previous_plots = True
        self.display_previous_subwindows = True
        self.show_legend = True
        self.show_axis_names = True
        self.name_of_axis_x = self.translation.selected_language.get(
            'axis_x', 'Axis X')
        self.name_of_axis_y = self.translation.selected_language.get(
            'axis_y', 'Axis Y')
        self.name_of_axis_z = self.translation.selected_language.get(
            'axis_z', 'Axis Z')
