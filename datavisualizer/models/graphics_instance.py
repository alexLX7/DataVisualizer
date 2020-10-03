import random
import numpy as np
import datavisualizer.models.translation as translation


class GraphicsInstance:
    def __init__(self):
        self.translation = translation.Translation()
        self.unique_id = None
        self.deleted = False

        self.table_deleted = False
        self.table_name = None
        self.table_id = None
        self.file_name = None

        self.color = None
        self.name = None
        self.visible = True
        self.original_type_of_creation = None
        self.contains_non_original_zero_values = False
        self.number_of_values_of_axis_x = None
        self.number_of_values_of_axis_y = None
        self.number_of_values_of_axis_z = None

        self.index_of_users_choice_in_context_menu_of_creation_type = None
        self.index_of_users_choice_in_options_of_list_to_show = 0

        self.list_of_lists_of_values_to_show = []  # list of 3 lists of lists to show

        # original list of all selected cells (raw row and column numbers)
        self.list_of_cells = []

        self.list_of_x_to_load = []  # list of cells to load from table for axis X
        self.list_of_y_to_load = []  # list of cells to load from table for axis Y
        self.list_of_z_to_load = []  # list of cells to load from table for axis Z

        # in-between data, contains values and raw row and column numbers
        self.list_of_x_y_z = []

        self.final_list_of_x_y_z = []  # final list of 3 lists of lists

    def set_name_of_graphical_instance(self, text):
        result = text
        max_number_of_chars = 50
        dots = '...'
        if len(text) > max_number_of_chars:
            len_minus_dots = max_number_of_chars - len(dots)
            result = text[0:len_minus_dots] + dots
        return result

    def _set_lists_to_load(self, list_of_x=[], list_of_y=[], list_of_z=[]):
        self.list_of_x_to_load = list_of_x
        self.list_of_y_to_load = list_of_y
        self.list_of_z_to_load = list_of_z

    def _method_21(self, list_of_cells):  # 21 means 2d, 1st users choice
        # set_as_clusters_of_rows_value_as_Y_column_index_as_X
        list_of_cells_of_x = []
        list_of_cells_of_y = []
        list_of_cells_of_z = []
        list_of_x_y_z = []

        dict_of_filtered_cells = dict()

        for cell in list_of_cells:
            if cell[1] in dict_of_filtered_cells:
                dict_of_filtered_cells[cell[1]].append(cell[0])
            else:
                dict_of_filtered_cells[cell[1]] = [cell[0]]

        for key in dict_of_filtered_cells:
            list_of_each_row = []
            for i, v in enumerate(dict_of_filtered_cells[key]):
                list_of_each_row.append([v, key])
            list_of_cells_of_y.append(list_of_each_row)

        for key in dict_of_filtered_cells:
            list_of_each_row = []
            for i, v in enumerate(dict_of_filtered_cells[key]):
                list_of_each_row.append(v)
            list_of_cells_of_x.append(list_of_each_row)

        for key in dict_of_filtered_cells:
            list_of_each_row = []
            for i, v in enumerate(dict_of_filtered_cells[key]):
                list_of_each_row.append(i + 1)
            list_of_cells_of_z.append(list_of_each_row)

        self._set_lists_to_load(list_of_y=list_of_cells_of_y)
        list_of_x_y_z.append(list_of_cells_of_x)
        list_of_x_y_z.append([])
        list_of_x_y_z.append(list_of_cells_of_z)

        return list_of_x_y_z

    def _method_22(self, list_of_cells):  # 22 means 2d, 2nd users choice
        # set_as_clusters_of_rows_1st_row_values_as_X_2nd_row_values_as_Y
        list_of_cells_of_x = []
        list_of_cells_of_y = []
        list_of_cells_of_z = []
        list_of_x_y_z = []

        dict_of_filtered_cells = dict()
        list_of_keys = []
        for cell in list_of_cells:
            if cell[1] in dict_of_filtered_cells:
                dict_of_filtered_cells[cell[1]].append(cell[0])
            else:
                dict_of_filtered_cells[cell[1]] = [cell[0]]
            list_of_keys.append(cell[1])
        # sort all keys
        list_of_keys = list(set(list_of_keys))

        if not len(list_of_keys) is 2:
            return None
        else:
            list_of_lengths_of_each_list = []
            for key in dict_of_filtered_cells:
                list_of_lengths_of_each_list.append(
                    len(dict_of_filtered_cells[key]))
            if list_of_lengths_of_each_list[0] is list_of_lengths_of_each_list[1]:
                for key in dict_of_filtered_cells:
                    if key is list_of_keys[0]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([v, key])
                        list_of_cells_of_y.append(list_of_each_row)
                    if key is list_of_keys[1]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([v, key])
                        list_of_cells_of_x.append(list_of_each_row)
            else:
                return None
        self._set_lists_to_load(
            list_of_x=list_of_cells_of_x,
            list_of_y=list_of_cells_of_y
        )

        for key in dict_of_filtered_cells:
            if key is list_of_keys[0]:
                list_of_each_row = []
                for i, v in enumerate(dict_of_filtered_cells[key]):
                    list_of_each_row.append(i + 1)
                list_of_cells_of_z.append(list_of_each_row)

        list_of_x_y_z.append([])
        list_of_x_y_z.append([])
        list_of_x_y_z.append(list_of_cells_of_z)
        return list_of_x_y_z

    def _method_23(self, list_of_cells):  # 23 means 2d, 3rd users choice
        # set_as_clusters_of_columns_value_as_Y_row_index_as_X
        list_of_cells_of_x = []
        list_of_cells_of_y = []
        list_of_cells_of_z = []
        list_of_x_y_z = []

        dict_of_filtered_cells = dict()

        for cell in list_of_cells:
            if cell[0] in dict_of_filtered_cells:
                dict_of_filtered_cells[cell[0]].append(cell[1])
            else:
                dict_of_filtered_cells[cell[0]] = [cell[1]]

        for key in dict_of_filtered_cells:
            list_of_each_row = []
            for i, v in enumerate(dict_of_filtered_cells[key]):
                list_of_each_row.append([key, v])
            list_of_cells_of_y.append(list_of_each_row)

        for key in dict_of_filtered_cells:
            list_of_each_row = []
            for i, v in enumerate(dict_of_filtered_cells[key]):
                list_of_each_row.append(v)
            list_of_cells_of_x.append(list_of_each_row)

        for key in dict_of_filtered_cells:
            list_of_each_row = []
            for i, v in enumerate(dict_of_filtered_cells[key]):
                list_of_each_row.append(i + 1)
            list_of_cells_of_z.append(list_of_each_row)

        self._set_lists_to_load(list_of_y=list_of_cells_of_y)
        list_of_x_y_z.append(list_of_cells_of_x)
        list_of_x_y_z.append([])
        list_of_x_y_z.append(list_of_cells_of_z)
        return list_of_x_y_z

    def _method_24(self, list_of_cells):  # 24 means 2d, 4th users choice
        # set_as_clusters_of_columns_1st_column_values_as_X_2nd_column_values_as_Y
        list_of_cells_of_x = []
        list_of_cells_of_y = []
        list_of_cells_of_z = []
        list_of_x_y_z = []

        dict_of_filtered_cells = dict()
        list_of_keys = []
        for cell in list_of_cells:
            if cell[0] in dict_of_filtered_cells:
                dict_of_filtered_cells[cell[0]].append(cell[1])
            else:
                dict_of_filtered_cells[cell[0]] = [cell[1]]
            list_of_keys.append(cell[0])

        list_of_keys = list(set(list_of_keys))

        if not len(list_of_keys) is 2:
            return list_of_x_y_z
        else:
            list_of_lengths_of_each_list = []
            for key in dict_of_filtered_cells:
                list_of_lengths_of_each_list.append(
                    len(dict_of_filtered_cells[key]))
            if list_of_lengths_of_each_list[0] is list_of_lengths_of_each_list[1]:
                for key in dict_of_filtered_cells:
                    if key is list_of_keys[0]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([key, v])
                        list_of_cells_of_y.append(list_of_each_row)
                    if key is list_of_keys[1]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([key, v])
                        list_of_cells_of_x.append(list_of_each_row)
            else:
                return None
        self._set_lists_to_load(
            list_of_x=list_of_cells_of_x,
            list_of_y=list_of_cells_of_y
        )
        for key in dict_of_filtered_cells:
            if key is list_of_keys[0]:
                list_of_each_row = []
                for i, v in enumerate(dict_of_filtered_cells[key]):
                    list_of_each_row.append(i + 1)
                list_of_cells_of_z.append(list_of_each_row)
        list_of_x_y_z.append([])
        list_of_x_y_z.append([])
        list_of_x_y_z.append(list_of_cells_of_z)
        return list_of_x_y_z

    def _method_31(self, list_of_cells):  # 31 means 3d, 1st users choice
        # set_selected_values_as_Z_numbers_of_columns_as_X_numbers_of_rows_as_Y
        list_of_cells_of_x = []
        list_of_cells_of_y = []
        list_of_cells_of_z = []
        list_of_x_y_z = []

        # for columns numbers
        d1 = dict()
        for cell in list_of_cells:
            if cell[0] in d1:
                d1[cell[0]].append(cell[1])
            else:
                d1[cell[0]] = [cell[1]]
        for key in d1:
            list_of_each_row = []
            for i, v in enumerate(d1[key]):
                list_of_each_row.append(v)
            list_of_cells_of_x.append(list_of_each_row)

        # for rows numbers
        d2 = dict()
        for cell in list_of_cells:
            if cell[1] in d2:
                d2[cell[1]].append(cell[0])
            else:
                d2[cell[1]] = [cell[0]]
        for key in d2:
            list_of_each_row = []
            for i, v in enumerate(d2[key]):
                list_of_each_row.append(v)
            list_of_cells_of_y.append(list_of_each_row)

        # z
        for key in d2:
            list_of_each_row = []
            for i, v in enumerate(d2[key]):
                list_of_each_row.append([v, key])
            list_of_cells_of_z.append(list_of_each_row)

        # transpose
        list_of_cells_of_x = np.array(list_of_cells_of_x).T.tolist()

        self._set_lists_to_load(list_of_z=list_of_cells_of_z)
        list_of_x_y_z.append(list_of_cells_of_x)
        list_of_x_y_z.append(list_of_cells_of_y)
        list_of_x_y_z.append([])
        return list_of_x_y_z

    def _method_32(self, list_of_cells):  # 32 means 3d, 2nd users choice
        # set_selected_values_as_Z_numbers_from_1_to_n_as_X_numbers_from_1_to_m_as_Y
        list_of_cells_of_x = []
        list_of_cells_of_y = []
        list_of_cells_of_z = []
        list_of_x_y_z = []

        # for columns numbers
        d1 = dict()
        for cell in list_of_cells:
            if cell[0] in d1:
                d1[cell[0]].append(cell[1])
            else:
                d1[cell[0]] = [cell[1]]
        for key in d1:
            list_of_each_row = []
            for i, v in enumerate(d1[key]):
                list_of_each_row.append(i + 1)
            list_of_cells_of_x.append(list_of_each_row)

        # for rows numbers
        d2 = dict()
        for cell in list_of_cells:
            if cell[1] in d2:
                d2[cell[1]].append(cell[0])
            else:
                d2[cell[1]] = [cell[0]]
        for key in d2:
            list_of_each_row = []
            for i, v in enumerate(d2[key]):
                list_of_each_row.append(i + 1)
            list_of_cells_of_y.append(list_of_each_row)

        # z
        for key in d2:
            list_of_each_row = []
            for i, v in enumerate(d2[key]):
                list_of_each_row.append([v, key])
            list_of_cells_of_z.append(list_of_each_row)

        # transpose
        list_of_cells_of_x = np.array(list_of_cells_of_x).T.tolist()

        self._set_lists_to_load(list_of_z=list_of_cells_of_z)
        list_of_x_y_z.append(list_of_cells_of_x)
        list_of_x_y_z.append(list_of_cells_of_y)
        list_of_x_y_z.append([])
        return list_of_x_y_z

    def _method_33(self, list_of_cells):  # 33 means 3d, 3rd users choice
        # set_as_clusters_of_rows_1st_row_values_as_X_2nd_row_values_as_Y_3rd_row_values_as_Z
        list_of_cells_of_x = []
        list_of_cells_of_y = []
        list_of_cells_of_z = []
        list_of_x_y_z = []

        dict_of_filtered_cells = dict()
        list_of_keys = []
        for cell in list_of_cells:
            if cell[1] in dict_of_filtered_cells:
                dict_of_filtered_cells[cell[1]].append(cell[0])
            else:
                dict_of_filtered_cells[cell[1]] = [cell[0]]
            list_of_keys.append(cell[1])

        list_of_keys = list(set(list_of_keys))

        if not len(list_of_keys) is 3:
            return list_of_x_y_z
        else:
            list_of_lengths_of_each_list = []
            for key in dict_of_filtered_cells:
                list_of_lengths_of_each_list.append(
                    len(dict_of_filtered_cells[key]))
            if list_of_lengths_of_each_list.count(list_of_lengths_of_each_list[0]) == len(list_of_lengths_of_each_list):
                for key in dict_of_filtered_cells:
                    if key is list_of_keys[0]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([v, key])
                        list_of_cells_of_x.append(list_of_each_row)
                    if key is list_of_keys[1]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([v, key])
                        list_of_cells_of_y.append(list_of_each_row)
                    if key is list_of_keys[2]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([v, key])
                        list_of_cells_of_z.append(list_of_each_row)
            else:
                return None
        self._set_lists_to_load(
            list_of_x=list_of_cells_of_x,
            list_of_y=list_of_cells_of_y,
            list_of_z=list_of_cells_of_z
        )
        list_of_x_y_z.append([])
        list_of_x_y_z.append([])
        list_of_x_y_z.append([])
        return list_of_x_y_z

    def _method_34(self, list_of_cells):  # 34 means 3d, 4th users choice
        # set_as_clusters_of_columns_1st_column_values_as_X_2nd_column_values_as_Y_3rd_column_values_as_Z
        list_of_cells_of_x = []
        list_of_cells_of_y = []
        list_of_cells_of_z = []
        list_of_x_y_z = []

        dict_of_filtered_cells = dict()
        list_of_keys = []
        for cell in list_of_cells:
            if cell[0] in dict_of_filtered_cells:
                dict_of_filtered_cells[cell[0]].append(cell[1])
            else:
                dict_of_filtered_cells[cell[0]] = [cell[1]]
            list_of_keys.append(cell[0])

        list_of_keys = list(set(list_of_keys))

        if not len(list_of_keys) is 3:
            return list_of_x_y_z
        else:
            list_of_lengths_of_each_list = []
            for key in dict_of_filtered_cells:
                list_of_lengths_of_each_list.append(
                    len(dict_of_filtered_cells[key]))
            if list_of_lengths_of_each_list.count(list_of_lengths_of_each_list[0]) == len(list_of_lengths_of_each_list):
                for key in dict_of_filtered_cells:
                    if key is list_of_keys[0]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([key, v])
                        list_of_cells_of_x.append(list_of_each_row)
                    if key is list_of_keys[1]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([key, v])
                        list_of_cells_of_y.append(list_of_each_row)
                    if key is list_of_keys[2]:
                        list_of_each_row = []
                        for i, v in enumerate(dict_of_filtered_cells[key]):
                            list_of_each_row.append([key, v])
                        list_of_cells_of_z.append(list_of_each_row)
            else:
                return None
        self._set_lists_to_load(
            list_of_x=list_of_cells_of_x,
            list_of_y=list_of_cells_of_y,
            list_of_z=list_of_cells_of_z,
        )
        list_of_x_y_z.append([])
        list_of_x_y_z.append([])
        list_of_x_y_z.append([])
        return list_of_x_y_z

    def _count_number_of_values_of_one_axis(self, list_of_lists):
        number_of_values_of_axis = 0
        for _, value_of_list_axis in enumerate(list_of_lists):
            number_of_values_of_axis += len(value_of_list_axis)
        return number_of_values_of_axis

    def set_number_of_values_of_each_axis(self):
        self.number_of_values_of_axis_x = self._count_number_of_values_of_one_axis(
            self.list_of_x_y_z[0])
        self.number_of_values_of_axis_y = self._count_number_of_values_of_one_axis(
            self.list_of_x_y_z[1])
        self.number_of_values_of_axis_z = self._count_number_of_values_of_one_axis(
            self.list_of_x_y_z[2])

    def set_values_by_users_choice(self, users_choice, list_of_cells):
        if users_choice is 21:
            self.original_type_of_creation = '2D'
            return self._method_21(list_of_cells)
        if users_choice is 22:
            self.original_type_of_creation = '2D'
            return self._method_22(list_of_cells)
        if users_choice is 23:
            self.original_type_of_creation = '2D'
            return self._method_23(list_of_cells)
        if users_choice is 24:
            self.original_type_of_creation = '2D'
            return self._method_24(list_of_cells)
        if users_choice is 31:
            self.original_type_of_creation = '3D: ' + \
                self.translation.selected_language.get(
                    'first_type', '1st type')
            return self._method_31(list_of_cells)
        if users_choice is 32:
            self.original_type_of_creation = '3D: ' + \
                self.translation.selected_language.get(
                    'first_type', '1st type')
            return self._method_32(list_of_cells)
        if users_choice is 33:
            self.original_type_of_creation = '3D: ' + \
                self.translation.selected_language.get(
                    'second_type', '2nd type')
            return self._method_33(list_of_cells)
        if users_choice is 34:
            self.original_type_of_creation = '3D: ' + \
                self.translation.selected_language.get(
                    'second_type', '2nd type')
            return self._method_34(list_of_cells)

    def randomize_color(self):
        def r(): return random.randint(100, 255)
        shade = random.randint(0, 2)
        if shade == 0:
            return '#%02X%02X%02X' % (r() // 10, r(), r())
        if shade == 1:
            return '#%02X%02X%02X' % (r(), r() // 10, r())
        if shade == 2:
            return '#%02X%02X%02X' % (r(), r(), r() // 10)
