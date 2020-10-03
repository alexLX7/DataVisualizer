import os
import sys
import ntpath
import pandas as pd
import sqlalchemy
import psycopg2
import datavisualizer.models.connection_object as co
import datavisualizer.models.custom_table_instance as cti


class ProjectInstanceOfSqlObject:
    def __init__(self, table_name):
        self.table_name = table_name
        self.list_of_custom_table_instances = []
        self.file_name = 'SQL object'
        self.path_to_icon = os.path.join(os.getcwd(), 'datavisualizer', 'resources', 'images', 'icon.sql.60x60.png')
        self.init()

    def init(self):
        self.connection_object = co.ConnectionObject()
        self._set_df_out_of_sql()

    def _set_df_out_of_sql(self):
        df = pd.read_sql_query(
            f"SELECT * FROM {self.table_name}",
            con=self.connection_object.connection
        )
        self._set_list_of_custom_table_instances(df)

    def _set_list_of_custom_table_instances(self, df):
        if not df.empty:
            custom_table_instance = cti.CustomTableInstance(
                df.fillna(0),
                self.table_name,
                self.file_name
            )
            self.list_of_custom_table_instances.append(custom_table_instance)
        self._close_connection()

    def _close_connection(self):
        try:
            self.connection_object.connection.close()
        except:
            pass
