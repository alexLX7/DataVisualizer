import psycopg2
import datavisualizer.models.json_handler as jh


class ConnectionObject:
    def __init__(self):
        self.dict_of_sql_config = {}
        self.connection = None
        self.init()

    def get_list_of_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(self.dict_of_sql_config['custom_select'])
        raw_list_of_tables = [item[0] for item in cursor.fetchall()]
        list_of_tables = list(set(raw_list_of_tables))
        return list_of_tables

    def init(self):
        jsonHandler = jh.JsonHandler()
        self.dict_of_sql_config = jsonHandler.load_data_from_config_sql_file()
        try:
            self.connection = psycopg2.connect(
                host=self.dict_of_sql_config["host"],
                database=self.dict_of_sql_config["database"],
                user=self.dict_of_sql_config["user"],
                password=self.dict_of_sql_config["password"])
        except:
            pass
