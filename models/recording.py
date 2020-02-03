""" ranking model to write to CSV

TODO (yoshiki) Rewrite to DB instead of CSV
"""

import collections
import csv
import os
import pathlib

RANKING_COLUMN_NAME = 'NAME'
RANKING_COLUMN_COUNT = 'COUNT'
RECORDING_CSV_FILE_PATH = 'record.csv'


class CsvModel(object):
    """Base csv model"""
    def __init__(self, csv_file):
        self.csv_file = csv_file
        if not os.path.exists(csv_file):
            pathlib.Path(csv_file).touch()

class RecordingModel(CsvModel):
    """Definition of class that generates ranking model to write to CSV"""
    def __init__(self, csv_file=None, *args, **kwargs):
        if not csv_file:
            csv_file = self.get_csv_file_path()
        super().__init__(csv_file, *args, **kwargs)
        self.column = [RANKING_COLUMN_NAME, RANKING_COLUMN_COUNT]
        self.data = collections.defaultdict(int)
        # self.load_data()

    def get_csv_file_path(self):
        """Set csv file path.

        Use csv path if set in settings, otherwise use default
        """
        csv_file_path = None
        try:
            import settings
            if settings.CSV_FILE_PATH:
                csv_file_path = settings.CSV_FILE_PATH
        except ImportError:
            pass

        if not csv_file_path:
            csv_file_path = RECORDING_CSV_FILE_PATH
        return csv_file_path

def main():
    recording = RecordingModel()


if __name__ == "__main__":
    main()