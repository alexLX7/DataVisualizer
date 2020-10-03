from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as matplotlibpyplot
from matplotlib import cm
import numpy as np
import datavisualizer.models.translation as translation
import datavisualizer.widgets.custom_widgets.global_info as global_info


class MPLTemplateSubWindow(QtWidgets.QWidget):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None):
        super(MPLTemplateSubWindow, self).__init__(parent)
        self.list_of_graphics_menus_instances = list_of_graphics_menus_instances
        self.dict_of_options = dict_of_options
        self.translation = translation.Translation()
        self.init()

    def init(self):
        self.figure = matplotlibpyplot.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.figure.clear()
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.set_axis_names()

    def set_axis_names(self):
        if self.dict_of_options['show_axis_names']:
            self.ax.set_xlabel(self.dict_of_options['name_of_axis_x'])
            self.ax.set_ylabel(self.dict_of_options['name_of_axis_y'])
            self.ax.set_zlabel(self.dict_of_options['name_of_axis_z'])

    def set_legend(self):
        if self.dict_of_options['show_legend']:
            self.ax.legend(loc='best')

    def set_curves(self):
        # set_curves() processes the self.list_of_graphics_menus_instances
        # That list contains of instances of GraphicsInstance class,
        # each instance of that class has list_of_lists_of_values_to_show
        # The structure of that list is:
        # [  # list_of_lists_of_values_to_show contains of 3 axis lists:
        #     [  # axis X with values as lists:
        #         [list_of_xs_with_index_0],  # values depend on type of creation
        #         [list_of_xs_with_index_1],
        #         [etc], [etc]  # number of axis X lists is the same as number of lists of Y and Z
        #     ],
        #     [  # axis Y with values as lists:
        #         [list_of_ys_with_index_0],  # has the same len as list_of_xs_with_index_0
        #         [list_of_ys_with_index_1],  # has the same len as list_of_xs_with_index_1
        #         [etc], [etc]
        #     ],
        #     [  # axis Z with values as lists:
        #         [list_of_zs_with_index_0],  # has the same len as list_of_xs_with_index_0
        #         [list_of_zs_with_index_1],  # has the same len as list_of_xs_with_index_1
        #         [etc], [etc]
        #     ]  # for better understanding I've made visual section of actual values:
        # ]  # actual values of each list are shown in options of each graphics menu instance
        #
        # This structure allows to visualize any two axis lists as 2D plot
        pass

    def safely_set_curves(self):
        try:
            self.set_curves()
        except:
            msg = global_info.GlobalInfo(
                self.translation.selected_language.get('msg_data_does_not_meet_req',
                                                       "Current data does not meet the requirements for this type of plot. In other words: the shape mismatch or data is too large to render using this type of plot. Please try a different type.")
            )

    def refresh_canvas(self):
        self.canvas.draw()


class MPL2DPlot(MPLTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(MPL2DPlot, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.figure.delaxes(self.ax)
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True)
        self.set_2d_axis_names()
        self.safely_set_curves()

    def set_2d_axis_names(self):
        if self.dict_of_options['show_axis_names']:
            self.ax.set_xlabel(self.dict_of_options['name_of_axis_x'])
            self.ax.set_ylabel(self.dict_of_options['name_of_axis_y'])

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        if i == 0:
                            self.ax.plot(
                                each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                                each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                                color=each_graphics_instance.color,
                                label=each_graphics_instance.name,
                            )
                        else:  # dont add a new label if we have more than 1 curve attached to the same gi
                            self.ax.plot(
                                each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                                each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                                color=each_graphics_instance.color,
                            )
                        self.set_legend()
        self.refresh_canvas()


class MPLScatterFirstType(MPLTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(MPLScatterFirstType, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.safely_set_curves()

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        if i == 0:
                            current_list_of_lists_of_x_axis = np.array(
                                each_graphics_instance.list_of_lists_of_values_to_show[0]).T.tolist()
                            current_list_of_lists_of_z_axis = np.array(
                                each_graphics_instance.list_of_lists_of_values_to_show[2]).T.tolist()
                            meshgrid_x, meshgrid_y = np.meshgrid(
                                np.array(current_list_of_lists_of_x_axis[0]),
                                np.array(
                                    each_graphics_instance.list_of_lists_of_values_to_show[1][0])
                            )
                            np_2d_array = np.array(
                                current_list_of_lists_of_z_axis)
                            self.ax.scatter(
                                meshgrid_x,
                                meshgrid_y,
                                np_2d_array,
                                color=each_graphics_instance.color,
                                label=each_graphics_instance.name,
                            )
                            self.set_legend()
        self.refresh_canvas()


class MPLScatterSecondType(MPLTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(MPLScatterSecondType, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.safely_set_curves()

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        if i == 0:
                            self.ax.scatter(
                                each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                                each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                                each_graphics_instance.list_of_lists_of_values_to_show[2][i],
                                color=each_graphics_instance.color,
                                label=each_graphics_instance.name,
                            )
                        else:
                            self.ax.scatter(
                                each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                                each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                                each_graphics_instance.list_of_lists_of_values_to_show[2][i],
                                color=each_graphics_instance.color,
                            )
                        self.set_legend()
        self.refresh_canvas()


class MPLSurfaceFirstType(MPLTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(MPLSurfaceFirstType, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.surf = None
        self.safely_set_curves()

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        if i == 0:
                            current_list_of_lists_of_x_axis = np.array(
                                each_graphics_instance.list_of_lists_of_values_to_show[0]).T.tolist()
                            current_list_of_lists_of_z_axis = np.array(
                                each_graphics_instance.list_of_lists_of_values_to_show[2]).T.tolist()
                            meshgrid_x, meshgrid_y = np.meshgrid(
                                np.array(current_list_of_lists_of_x_axis[0]),
                                np.array(
                                    each_graphics_instance.list_of_lists_of_values_to_show[1][0])
                            )
                            np_2d_array = np.array(
                                current_list_of_lists_of_z_axis)
                            self.surf = self.ax.plot_surface(
                                meshgrid_x,
                                meshgrid_y,
                                np_2d_array,
                                color=each_graphics_instance.color,
                                label=each_graphics_instance.name,
                            )
                            self.surf._facecolors2d = self.surf._facecolors3d
                            self.surf._edgecolors2d = self.surf._edgecolors3d
                            if self.dict_of_options['show_legend']:
                                self.ax.legend(loc='best')
        self.refresh_canvas()


class MPLSurfaceSecondType(MPLTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(MPLSurfaceSecondType, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.surf = None
        self.safely_set_curves()

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        if i == 0:
                            np_2d_array = np.array(
                                [each_graphics_instance.list_of_lists_of_values_to_show[2][0],
                                 each_graphics_instance.list_of_lists_of_values_to_show[2][0]]
                            )
                            self.surf = self.ax.plot_surface(
                                each_graphics_instance.list_of_lists_of_values_to_show[0][0],
                                each_graphics_instance.list_of_lists_of_values_to_show[1][0],
                                np_2d_array,
                                color=each_graphics_instance.color,
                                label=each_graphics_instance.name,
                            )
                            self.surf._facecolors2d = self.surf._facecolors3d
                            self.surf._edgecolors2d = self.surf._edgecolors3d
                            if self.dict_of_options['show_legend']:
                                self.ax.legend(loc='best')
        self.refresh_canvas()


class MPLWireframeFirstType(MPLTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(MPLWireframeFirstType, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.safely_set_curves()

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        if i == 0:
                            current_list_of_lists_of_x_axis = np.array(
                                each_graphics_instance.list_of_lists_of_values_to_show[0]).T.tolist()
                            current_list_of_lists_of_z_axis = np.array(
                                each_graphics_instance.list_of_lists_of_values_to_show[2]).T.tolist()
                            meshgrid_x, meshgrid_y = np.meshgrid(
                                np.array(current_list_of_lists_of_x_axis[0]),
                                np.array(
                                    each_graphics_instance.list_of_lists_of_values_to_show[1][0])
                            )
                            np_2d_array = np.array(
                                current_list_of_lists_of_z_axis)
                            self.ax.plot_wireframe(
                                meshgrid_x,
                                meshgrid_y,
                                np_2d_array,
                                color=each_graphics_instance.color,
                                label=each_graphics_instance.name,
                            )
                            self.set_legend()
        self.refresh_canvas()


class MPLWireframeSecondType(MPLTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(MPLWireframeSecondType, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.safely_set_curves()

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        if i == 0:
                            np_2d_array = np.array(
                                [each_graphics_instance.list_of_lists_of_values_to_show[2][0],
                                 each_graphics_instance.list_of_lists_of_values_to_show[2][0]]
                            )
                            self.ax.plot_wireframe(
                                each_graphics_instance.list_of_lists_of_values_to_show[0][0],
                                each_graphics_instance.list_of_lists_of_values_to_show[1][0],
                                np_2d_array,
                                color=each_graphics_instance.color,
                                label=each_graphics_instance.name,
                            )
                            self.set_legend()
        self.refresh_canvas()
