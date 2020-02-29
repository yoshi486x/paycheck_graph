import collections
import json
import numpy as np
import os
import pandas as pd
import pathlib
import pprint
pp = pprint.PrettyPrinter(indent=4, width=20)

JSON_DIR_PATH = 'data/output/json'
GRAPHS_DIR_PATH = 'data/output/graphs_and_charts'
INCOME_GRAPH_NAME = 'income_timechart.png'

class JsonModel(object):
    def __init__(self, filename, json_file):
        if not json_file:
            json_file = self.get_json_file_path(filename)
        if not os.path.exists(json_file):
            pathlib.Path(json_file).touch()
        self.filename = filename
        self.json_file = json_file


class VisualizingModel(object):

    def __init__(self, filenames, base_dir=None, dataframe=None, figure=None):
        if not base_dir:
            base_dir = self.get_base_dir_path()
        self.base_dir = base_dir
        if not filenames:
            filenames = self.get_json_file_path() 
        self.filenames = filenames
        self.dataframe = dataframe
        self.figure = figure
        self.graphs = INCOME_GRAPH_NAME

    def create_base_table(self):
        """Create base tablefor """
        df = self.dataframe
        dataframes = []

        # Loop
        for filename in self.filenames:
            dates, keys, values, indexes = [], [], [], []

            file_path = pathlib.Path(JSON_DIR_PATH, filename)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            
            """Single key extraction"""
            dates, keys, values = [], [], []
            date = data['summary']['支給年月日']
            for key, value in data['incomes'].items():
                values.append(value)
                keys.append(key)
                dates.append(date)
            df = pd.DataFrame({'date': dates, 'type': keys, 'income': values})
            dataframes.append(df)

        # Combine tables of each json file
        df = pd.concat(dataframes)
        df = df.pivot(index='date', columns='type', values='income')

        """TODO Maybe this func should be placed separately"""
        try:
            try:
                import camouflage
            except:
                from models import camouflage
            df = camouflage.camouflage(df)
        except:
            pass
        
        self.dataframe = df

    def get_base_dir_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_json_file_path(self):
        """Set json file path.
        Use json path if set in settings, otherwise use default.
        
        :type filename: str
        :rtype json_file_path: str
        """
        json_file_path = None
        try:
            import settings
            if settings.JSON_FILE_PATH:
                json_file_path = settings.JSON_FILE_PATH
        except ImportError:
            pass

        filenames = []
        json_full_dir_path = pathlib.Path(self.base_dir, JSON_DIR_PATH)

        if json_file_path is None:
            for item in os.listdir(json_full_dir_path):
                filenames.append(item)
        return filenames

    def save_graph_to_image(self):
        file_path = pathlib.Path(GRAPHS_DIR_PATH, self.graphs)
        ax = self.dataframe.plot(
            figsize=(15, 10), kind='bar', stacked=True, grid=True, sharey=False,
            title='Income breakdown (2018/09 - 2019/12) **Sample data was used for this graph**',
            )
        ax.set_ylabel('amount of income')
        fig = ax.get_figure()
        fig.savefig(file_path)

    def sort_table(self):

        try:
            import sorting
        except:
            from models import sorting
        
        df = sorting.sort_table(self.dataframe)
        self.dataframe = df


def main():
    visual = VisualizingModel(None)
    visual.create_base_table()
    visual.sort_table()
    visual.save_graph_to_image()


if __name__ == "__main__":
    main()