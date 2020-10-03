import os
import sys
import ntpath
import pandas as pd
import datavisualizer.models.custom_table_instance as cti


class ProjectInstance:
    def __init__(self, input_path, type_of_file):
        self.input_path = input_path
        self.type_of_file = type_of_file
        self.list_of_custom_table_instances = []
        self.path_to_icon = None
        self.path_to_csv_icon = os.path.join(os.getcwd(), 'datavisualizer', 'resources', 'images', 'icon.csv.60x60.png')
        self.path_to_excel_icon = os.path.join(os.getcwd(), 'datavisualizer', 'resources', 'images', 'icon.excel.60x60.png')
        self.plain_text_csv = 'csv'
        self.plain_text_excel = 'excel'
        self.file_name = self._set_file_name()
        self.init()

    def init(self):
        if self.type_of_file is self.plain_text_excel:
            self.path_to_icon = self.path_to_excel_icon
            self._set_list_of_df_out_of_excel()
        if self.type_of_file is self.plain_text_csv:
            self.path_to_icon = self.path_to_csv_icon
            self._set_list_of_df_out_of_csv()

    def _set_file_name(self):
        head, tail = ntpath.split(self.input_path)
        return tail or ntpath.basename(head)

    def _filter_extension_out_of_csv_file_name(self):
        return os.path.splitext(self.file_name)[0]

    def _set_list_of_df_out_of_excel(self):
        xl_file = pd.ExcelFile(self.input_path)
        for v in xl_file.sheet_names:
            df = xl_file.parse(v, header=None)
            if not df.empty:
                custom_table_instance = cti.CustomTableInstance(
                    df.fillna(0), v, self.file_name)
                self.list_of_custom_table_instances.append(
                    custom_table_instance)

    def _set_list_of_df_out_of_csv(self):
        df = pd.read_csv(self.input_path, header=None)
        if not df.empty:
            custom_table_instance = cti.CustomTableInstance(
                df.fillna(0),
                self._filter_extension_out_of_csv_file_name(),
                self.file_name)
            self.list_of_custom_table_instances.append(custom_table_instance)
