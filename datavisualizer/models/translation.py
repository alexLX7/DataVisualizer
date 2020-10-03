import os
import datavisualizer.models.json_handler as jh


class Translation:
    def __init__(self):
        self.path_of_english_json_file = os.path.join(os.getcwd(), 'datavisualizer', 'resources', 'translation', 'english.json')
        self.path_of_russian_json_file = os.path.join(os.getcwd(), 'datavisualizer', 'resources', 'translation', 'russian.json')
        self.dict_of_english = dict()
        self.dict_of_russian = dict()
        self.selected_language = None
        self._set_dicts_of_languages()
        self._set_selected_language()

    def _set_dicts_of_languages(self):
        json_handler = jh.JsonHandler()
        self.dict_of_english = json_handler.load_language_from_json_file(
            self.path_of_english_json_file)
        self.dict_of_russian = json_handler.load_language_from_json_file(
            self.path_of_russian_json_file)

    def _set_selected_language(self):
        json_handler = jh.JsonHandler()
        data = json_handler.load_data_from_config_file()
        if data['language'] == 'english':
            self.selected_language = self.dict_of_english
        if data['language'] == 'russian':
            self.selected_language = self.dict_of_russian
