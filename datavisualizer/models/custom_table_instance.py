import datavisualizer.models.pandas_model as pm


class CustomTableInstance:
    def __init__(self, data, table_name, file_name):
        self.unique_id = None
        self.deleted = False
        self.table_name = table_name
        self.table_model = pm.PandasModel(data)
        self.table_view = None
        self.file_name = file_name
        self.sub_window = None
