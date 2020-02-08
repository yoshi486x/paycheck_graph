import collections
import csv
import datetime
import json
import os
import pathlib
import string
import subprocess
import sys

try:
    from models import data_model
except ModuleNotFoundError:
    import data_model

EMPLOYEE_INFO_INDEX_DELTA = 6   # 3 * 2
DATA_NAME = 'data'
HOME_PATH = pathlib.Path(os.getcwd())
TEXT_FILE_NAME = 'output.txt'

class Formatter(data_model.DataModel):
    
    def __init__(self):
        super().__init__()
        self.json = str()

    def dict2json_file(self, datasource='organized_data.json'):
        """TODO:(yoshiki-11) Import from views module"""
        data_json = json.dumps(self.data, ensure_ascii=False, indent=4)
        data_path = HOME_PATH / datasource
        with open(data_path, 'w') as json_file:
            json_file.write(data_json)

    def format_from_data(self):
        print('self.data:', self.data[DATA_NAME])
        for data in self.data[DATA_NAME]:
            is_digit = self.string2digit(**data)
            data.update(is_digit)

    def load_json_as_dict(self):
        data_path = HOME_PATH / 'data.json'
        with open(data_path, 'r') as json_file:
            template = string.Template(json_file.read())
        self.data = json.loads(template.substitute())

    def string2digit(self, **kwargs):
        keys, values = [], []

        for k, v in kwargs.items():
            if type(v) != (int or float):
                if v.replace(',', '').isdigit() is True:
                    keys.append(k)
                    values.append(int(v.replace(',', '')))
                elif v.replace('.', '').isdigit() is True:
                    keys.append(k)
                    values.append(float(v))
            # print(k, type(k), v, type(v))
        return dict(zip(keys, values))