from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph import *
import datavisualizer.models.translation as translation
import datavisualizer.widgets.custom_widgets.global_info as global_info


class PyqtgraphTemplateSubWindow(QtWidgets.QWidget):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None):
        super(PyqtgraphTemplateSubWindow, self).__init__(parent)
        pg.setConfigOption('background', (255, 255, 255))
        pg.setConfigOption('foreground', (30, 30, 30))
        pg.setConfigOptions(antialias=True)
        self.translation = translation.Translation()
        self.list_of_graphics_menus_instances = list_of_graphics_menus_instances
        self.dict_of_options = dict_of_options
        self.init()

    def init(self):
        self.plot = pg.GraphicsLayoutWidget()
        self.layout = QtGui.QGridLayout(self)
        self.label = pg.LabelItem(justify='center')
        self.label.setText("")
        self.plot.addItem(self.label)
        self.layout.addWidget(self.plot, 1, 0)
        self.first_plot = self.plot.addPlot(row=1, col=0)
        self.first_plot.setMenuEnabled(False)
        for each_ax in self.first_plot.axes:
            self.first_plot.getAxis(each_ax).setGrid(255)
        self.v_cross_line = pg.InfiniteLine(angle=90, movable=False)
        self.h_cross_line = pg.InfiniteLine(angle=0, movable=False)
        self.first_plot.addItem(self.v_cross_line, ignoreBounds=True)
        self.first_plot.addItem(self.h_cross_line, ignoreBounds=True)
        self.scene = self.first_plot.scene()
        self.scene.sigMouseMoved.connect(self.mouse_moved)
        if self.dict_of_options['show_legend']:
            self.first_plot.addLegend()
        self.set_axis_names()

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

    def set_axis_names(self):
        if self.dict_of_options['show_axis_names']:
            self.first_plot.setLabel(
                'bottom', self.dict_of_options['name_of_axis_x'])
            self.first_plot.setLabel(
                'left', self.dict_of_options['name_of_axis_y'])

    def set_legend_item(self, legend_item):
        self.first_plot.addItem(legend_item)

    def _set_legend_item(self, name, color):
        legend_item = pg.PlotDataItem(
            name=' - ' + str(name),
            pen=pg.mkPen(color, width=2),
            symbol=None,
            symbolBrush=color,
            symbolSize=16)
        return legend_item

    def mouse_moved(self, evt):
        self.label.setText(
            "x = {:.5f}; y = {:.5f}".format(
                self.first_plot.vb.mapSceneToView(evt).x(),
                self.first_plot.vb.mapSceneToView(evt).y())
        )
        self.v_cross_line.setPos(self.first_plot.vb.mapSceneToView(evt).x())
        self.h_cross_line.setPos(self.first_plot.vb.mapSceneToView(evt).y())


class PyqtgraphSimplePlot(PyqtgraphTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(PyqtgraphSimplePlot, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.set_curves()

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        curve = self.first_plot.plot(
                            x=each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                            y=each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                            pen=pg.mkPen(
                                each_graphics_instance.color, width=2),
                            symbolBrush=each_graphics_instance.color,
                            symbolPen=each_graphics_instance.color,
                            symbol='o', clickable=False
                        )
                        if self.dict_of_options['show_legend']:
                            # we add label only once (for each graphics_instance)
                            if i == 0:
                                legend_item = self._set_legend_item(
                                    each_graphics_instance.name,
                                    each_graphics_instance.color
                                )
                                self.set_legend_item(legend_item)


class PyqtgraphAdvancedPlot(PyqtgraphTemplateSubWindow):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(PyqtgraphAdvancedPlot, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.vertical_line = None
        self.list_of_scatter_plot_items = []
        self.list_of_clicked_points = []
        self.list_of_curves = []
        self.list_of_texts = []
        self.set_curves()
        self.set_scatter_plot_items()

    def set_scatter_plot_items(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        s1 = pg.ScatterPlotItem(
                            size=10,
                            pen=pg.mkPen(each_graphics_instance.color),
                            brush=pg.mkBrush(each_graphics_instance.color)
                        )
                        s1.addPoints(
                            x=each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                            y=each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                            pen=pg.mkPen(
                                each_graphics_instance.color, width=2),
                        )
                        s1.sigClicked.connect(
                            self._scatter_plot_item_clicked)
                        self.first_plot.addItem(s1)
                        self.list_of_scatter_plot_items.append(s1)

    def set_curves(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        curve = self.first_plot.plot(
                            x=each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                            y=each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                            pen=pg.mkPen(
                                each_graphics_instance.color, width=2),
                            clickable=True,
                        )
                        curve.curve.setClickable(True)
                        curve.sigClicked.connect(self._curve_clicked)
                        self.list_of_curves.append(
                            [
                                curve, each_graphics_instance.color, False,
                                each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                                each_graphics_instance.list_of_lists_of_values_to_show[1][i]
                            ]
                        )
                        if self.dict_of_options['show_legend']:
                            if i == 0:
                                legend_item = self._set_legend_item(
                                    each_graphics_instance.name,
                                    each_graphics_instance.color
                                )
                                self.set_legend_item(legend_item)

    def _curve_clicked(self, curve):
        if self.list_of_curves:
            for i, c in enumerate(self.list_of_curves):
                if c[0] is curve:
                    if c[2] == True:  # if curve is selected:
                        c[0].setPen(c[1], width=2)
                        c[2] = False  # next action will be deselection
                    else:
                        c[0].setPen(c[1], width=8)
                        c[2] = True  # next action will be selection

    def _get_number_of_selected_curves(self):
        counter = 0
        if self.list_of_curves:
            for i, c in enumerate(self.list_of_curves):
                if c[2]:
                    counter += 1
        return counter

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()
        deselect_all_points = menu.addAction(
            self.translation.selected_language.get(
                'deselect_all_points', 'Deselect all points')
        )
        deselect_all_curves = menu.addAction(
            self.translation.selected_language.get(
                'deselect_all_curves', 'Deselect all curves')
        )
        create_line_to_measure_distance = menu.addAction(
            self.translation.selected_language.get(
                'create_line_to_measure_distance', 'Create line to measure distance')
        )
        delete_line_to_measure_distance = menu.addAction(
            self.translation.selected_language.get(
                'delete_line_to_measure_distance', 'Delete line to measure distance')
        )
        if self._get_number_of_selected_curves() is 2:
            create_line_to_measure_distance.setDisabled(False)
        else:
            create_line_to_measure_distance.setDisabled(True)

        if self.vertical_line:
            delete_line_to_measure_distance.setDisabled(False)
        else:
            delete_line_to_measure_distance.setDisabled(True)

        action = menu.exec_(QtGui.QCursor.pos())
        if action == deselect_all_curves:
            if self.list_of_curves:
                for i, c in enumerate(self.list_of_curves):
                    c[0].setPen(c[1], width=2)
                    c[2] = False  # next action will be selection
        if action == deselect_all_points:
            if self.list_of_clicked_points:
                for p in self.list_of_clicked_points:
                    p.resetPen()
            if self.list_of_texts:
                for i, v in enumerate(self.list_of_texts):
                    self.first_plot.removeItem(v)
            self.list_of_texts.clear()
        if action == create_line_to_measure_distance:
            self.create_line_to_measure_distance()
        if action == delete_line_to_measure_distance:
            if self.vertical_line:
                self.first_plot.removeItem(self.vertical_line)
                self.vertical_line = None

    def is_each_list_of_xs_sorted(self, list_of_xs):
        list_of_sorted_lists = []
        for i, v in enumerate(list_of_xs):
            list_of_sorted_lists.append(sorted(v))
        if list_of_sorted_lists == list_of_xs:
            return True
        return False

    def create_line_to_measure_distance(self):
        if self.vertical_line:
            self.first_plot.removeItem(self.vertical_line)
            self.vertical_line = None

        list_of_xs = []
        list_of_ys = []
        if self.list_of_curves:
            for i, c in enumerate(self.list_of_curves):
                if c[2]:
                    list_of_xs.append(c[3])
                    list_of_ys.append(c[4])

        if not self.is_each_list_of_xs_sorted(list_of_xs):
            msg = GlobalInfo(
                self.translation.selected_language.get('msg_unsorted_data_on_x_axis',
                                                       "Selected curves have unsorted data on X axis. Line to measure cannot be created.")
            )
            return

        self.vertical_line = pg.InfiniteLine(
            pos=min(list_of_xs[0] + list_of_xs[1]),
            movable=True, angle=90,
            pen=pg.mkPen('y', width=4),
            label='x={value:0.2f}',
            labelOpts={
                'position': 0.1,
                'color': (0, 0, 0),
                'fill': (200, 200, 200, 50), 'movable': True
            }
        )
        self.first_plot.addItem(self.vertical_line)
        self._connect_ver(list_of_xs, list_of_ys)

    def _connect_ver(self, list_of_xs, list_of_ys):

        def vertical_line_dragged():
            current_vertical_x = self.vertical_line.getPos()[0]
            list_of_current_ys = \
                self._process_distance_between_two_selected_curves(
                    current_vertical_x, list_of_xs, list_of_ys
                )
            tmp_y1 = None
            tmp_y2 = None
            # it is a try because of [0] and [1] requests of list
            try:
                tmp_y1 = list_of_current_ys[0]
                tmp_y2 = list_of_current_ys[1]
                general_ys_difference = abs(tmp_y1 - tmp_y2)

                self.vertical_line.label.setPlainText(
                    'x: ' + str(round(current_vertical_x, 8)) +
                    '\ny1: ' + str(round(list_of_current_ys[0], 8)) +
                    '\ny2: ' + str(round(list_of_current_ys[1], 8)) +
                    '\n|y1 - y2| = ' + str(round(general_ys_difference, 8))
                )
            except:
                pass
        self.vertical_line.sigPositionChangeFinished.connect(
            vertical_line_dragged)

    def _process_distance_between_two_selected_curves(self, current_vertical_x, list_of_xs, list_of_ys):
        list_of_current_ys = []
        if (current_vertical_x < min(list_of_xs[0] + list_of_xs[1])
                or current_vertical_x > max(list_of_xs[0] + list_of_xs[1])):
            return None
        for i, v in enumerate(list_of_xs):
            nearest_value_x = min(
                v, key=lambda _x: abs(_x - current_vertical_x))
            index_of_nearest_value = v.index(nearest_value_x)
            second_nearest_value_x = None
            index_of_second_nearest_value_x = None
            difference_1 = None
            difference_2 = None
            # these are 'try's because of requests of lists indexes
            try:
                difference_1 = abs(current_vertical_x -
                                   v[index_of_nearest_value + 1])
            except:
                difference_1 = None

            try:
                difference_2 = abs(current_vertical_x -
                                   v[index_of_nearest_value - 1])
            except:
                difference_2 = None

            if difference_1 and not difference_2:  # border case
                second_nearest_value_x = v[index_of_nearest_value + 1]
                index_of_second_nearest_value_x = v.index(
                    second_nearest_value_x)

            if not difference_1 and difference_2:  # border case
                second_nearest_value_x = v[index_of_nearest_value - 1]
                index_of_second_nearest_value_x = v.index(
                    second_nearest_value_x)

            if difference_1 and difference_2:  # both are valid indexes
                if difference_1 < difference_2:
                    second_nearest_value_x = v[index_of_nearest_value + 1]
                else:
                    second_nearest_value_x = v[index_of_nearest_value - 1]
                index_of_second_nearest_value_x = v.index(
                    second_nearest_value_x)
            try:
                _y1 = list_of_ys[i][index_of_nearest_value]
                _y2 = list_of_ys[i][index_of_second_nearest_value_x]
                _x1 = nearest_value_x
                _x2 = second_nearest_value_x
                if current_vertical_x < min(_x1, _x2) or current_vertical_x > max(_x1, _x2):
                    return None
                else:
                    _k = (_y1 - _y2) / (_x1 - _x2)
                    _b = _y2 - _k*_x2
                    current_y_for_this_curve = _k * current_vertical_x + _b
                    list_of_current_ys.append(current_y_for_this_curve)
            except:
                pass
        return list_of_current_ys

    def _scatter_plot_item_clicked(self, plot, points):
        for p in self.list_of_clicked_points:
            p.resetPen()
        for i, v in enumerate(points):
            text = pg.TextItem(
                text=str(v.viewPos().x()) + "; " + str(v.viewPos().y()),
                border="#000000", color="#000000",  # black foreground
                fill=(242, 242, 242)  # white background
            )
            text.setPos(v.viewPos().x(), v.viewPos().y())
            self.first_plot.addItem(text)
            self.list_of_texts.append(text)
        self.list_of_clicked_points = points


class PyqtgraphLinkedYPlot(PyqtgraphAdvancedPlot):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(PyqtgraphLinkedYPlot, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.init_second_plot()

    def init_second_plot(self):
        self.second_plot = self.plot.addPlot(
            name="Plot 2", row=1, col=1)
        self.second_plot.setLabel('left', "Plot 2: Y linked with Plot1")
        self.second_plot.setMenuEnabled(False)
        for each_ax in self.second_plot.axes:
            self.second_plot.getAxis(each_ax).setGrid(255)
        self.second_plot.setYLink(self.first_plot)
        self.set_axis_names_second_plot()
        self.set_curves_in_second_plot()

    def set_axis_names_second_plot(self):
        if self.dict_of_options['show_axis_names']:
            self.second_plot.setLabel(
                'bottom', self.dict_of_options['name_of_axis_x'])
            self.second_plot.setLabel(
                'left', self.dict_of_options['name_of_axis_y'])

    def set_curves_in_second_plot(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        curve = self.second_plot.plot(
                            x=each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                            y=each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                            pen=pg.mkPen(
                                each_graphics_instance.color, width=2),
                            symbolBrush=each_graphics_instance.color,
                            symbolPen=each_graphics_instance.color,
                            symbol='o',
                        )


class PyqtgraphLinkedXPlot(PyqtgraphAdvancedPlot):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(PyqtgraphLinkedXPlot, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.init_second_plot()

    def init_second_plot(self):
        self.second_plot = self.plot.addPlot(
            name="Plot 2", title="Plot 2: X linked with Plot 1", row=2, col=0)
        self.second_plot.setMenuEnabled(False)
        for each_ax in self.second_plot.axes:
            self.second_plot.getAxis(each_ax).setGrid(255)
        self.second_plot.setXLink(self.first_plot)
        self.set_axis_names_second_plot()
        self.set_curves_in_second_plot()

    def set_axis_names_second_plot(self):
        if self.dict_of_options['show_axis_names']:
            self.second_plot.setLabel(
                'bottom', self.dict_of_options['name_of_axis_x'])
            self.second_plot.setLabel(
                'left', self.dict_of_options['name_of_axis_y'])

    def set_curves_in_second_plot(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        curve = self.second_plot.plot(
                            x=each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                            y=each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                            pen=pg.mkPen(
                                each_graphics_instance.color, width=2),
                            symbolBrush=each_graphics_instance.color,
                            symbolPen=each_graphics_instance.color,
                            symbol='o',
                        )


class PyqtgraphDoublePlot(PyqtgraphAdvancedPlot):
    def __init__(self, list_of_graphics_menus_instances, dict_of_options, parent=None, **kwargs):
        super(PyqtgraphDoublePlot, self).__init__(
            list_of_graphics_menus_instances, dict_of_options, parent, **kwargs)
        self.init_double()
        self.set_axis_names_second_plot()
        self.set_curves_double()

    def init_double(self):
        self.second_plot = self.plot.addPlot(row=2, col=0)
        self.second_plot.setMenuEnabled(False)
        for each_ax in self.second_plot.axes:
            self.second_plot.getAxis(each_ax).setGrid(255)
        self.x_min_region = 0
        self.x_max_region = 1
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        self.second_plot.addItem(self.region, ignoreBounds=True)

        def update():
            self.region.setZValue(10)
            minX, maxX = self.region.getRegion()
            self.first_plot.setXRange(minX, maxX, padding=0)

        self.region.sigRegionChanged.connect(update)

        def updateRegion(window, viewRange):
            rgn = viewRange[0]
            self.region.setRegion(rgn)

        self.first_plot.sigRangeChanged.connect(updateRegion)
        self.region.setRegion([self.x_min_region, self.x_max_region])

    def _update_x_min_region_value(self, _list: list):
        _min = min(_list)
        if _min < self.x_min_region:
            self.x_min_region = _min

    def _update_x_max_region_value(self, _list: list):
        _max = max(_list)
        if _max > self.x_max_region:
            self.x_max_region = _max

    def set_axis_names_second_plot(self):
        if self.dict_of_options['show_axis_names']:
            self.second_plot.setLabel(
                'bottom', self.dict_of_options['name_of_axis_x'])
            self.second_plot.setLabel(
                'left', self.dict_of_options['name_of_axis_y'])

    def set_curves_double(self):
        for index_of_instance, each_graphics_instance in enumerate(self.list_of_graphics_menus_instances):
            if not each_graphics_instance.deleted and not each_graphics_instance.table_deleted:
                if each_graphics_instance.visible:
                    for i, v in enumerate(each_graphics_instance.list_of_lists_of_values_to_show[0]):
                        curve = self.second_plot.plot(
                            x=each_graphics_instance.list_of_lists_of_values_to_show[0][i],
                            y=each_graphics_instance.list_of_lists_of_values_to_show[1][i],
                            pen=pg.mkPen(
                                each_graphics_instance.color, width=2),
                            symbolBrush=each_graphics_instance.color,
                            symbolPen=each_graphics_instance.color,
                            symbol='o',
                        )
                        self._update_x_min_region_value(
                            each_graphics_instance.list_of_lists_of_values_to_show[0][i])
                        self._update_x_max_region_value(
                            each_graphics_instance.list_of_lists_of_values_to_show[0][i])
        self.region.setRegion([self.x_min_region, self.x_max_region])
