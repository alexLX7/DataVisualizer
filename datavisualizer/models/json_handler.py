import json
import os


class JsonHandler:
    def __init__(self):
        super().__init__()
        self.config_file = os.path.join(os.getcwd(), 'datavisualizer', 'config', 'config.json')
        self.config_sql_file = os.path.join(os.getcwd(), 'datavisualizer', 'config', 'config_sql.json')

    def write_data_to_config_file(self, data):
        with open(self.config_file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, sort_keys=False, ensure_ascii=False)

    def load_data_from_config_file(self):
        with open(self.config_file, encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def load_data_from_config_sql_file(self):
        with open(self.config_sql_file, encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def load_language_from_json_file(self, file):
        with open(file, encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
