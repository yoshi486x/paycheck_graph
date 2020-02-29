import csv
import os
import pathlib
import subprocess
import sys

EXEC_CMD = 'pdf2txt.py'
OUTPUT_DIR_PATH = 'data/output/temp'
PDF_DIR_PATH = 'data/pdf'
PDF_FILENAME_NAME = 'FILENAME'

# class CsvModel(object):
#     """Base csv model."""
#     def __init__(self, csv_file):
#         self.csv_file = csv_file
#         if not os.path.exists(csv_file):
#             pathlib.Path(csv_file).touch()


# class RankingModel(CsvModel):
#     """Definition of class that generates ranking model to write to CSV"""
#     def __init__(self, csv_file=None, *args, **kwargs):
#         if not csv_file:
#             csv_file = self.get_csv_file_path()
#         super().__init__(csv_file, *args, **kwargs)
#         self.column = [RANKING_COLUMN_NAME, RANKING_COLUMN_COUNT]
#         self.data = collections.defaultdict(int)
#         self.load_data()


class PdfModel(object):
    """Base pdf model"""
    def __init__(self, filenames):
        self.filenames = filenames

class PdfReader(PdfModel):
    def __init__(self, filenames=None, base_dir=None):
        super().__init__(filenames=filenames)
        if not base_dir:
            base_dir = self.get_base_dir_path()
        self.base_dir = base_dir

    def convert_pdf_to_txt(self, input_file, output_file):
        """Call pdf2text.py
        :type input_file :str
        :type output_file :str
        """
        subprocess.call([EXEC_CMD, '-V', '-o', str(output_file), str(input_file)])

    def get_base_dir_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_pdf_dir(self, filename, suffix='.pdf'):
        """Organize input pdf path info"""
        input_full_dir_path = pathlib.Path(self.base_dir, PDF_DIR_PATH)
        return pathlib.Path(input_full_dir_path, filename).with_suffix(suffix)

    def get_txt_dir(self, filename, suffix='.txt'):
        """Organize output txt path info"""
        output_full_dir_path = pathlib.Path(self.base_dir, OUTPUT_DIR_PATH)
        output_filename, _ = os.path.splitext(filename)
        return pathlib.Path(output_full_dir_path, output_filename).with_suffix(suffix)


class InputQueue(object):
    def __init__(self, base_dir=None, all_files=None, pdf_files=None):
        if not base_dir:
            base_dir = self.get_base_dir_path()
        self.base_dir = base_dir
        self.all_files = all_files
        self.pdf_files = pdf_files
    
    def get_base_dir_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def load_pdf_filenames(self, all_files=list):
        """List all pdf files in designated directory"""
        all_files = []
        pdf_full_dir_path = pathlib.Path(self.base_dir, PDF_DIR_PATH)
        self.pdf_files = os.listdir(pdf_full_dir_path)

        for item in os.listdir(pdf_full_dir_path):
            filename, _ = os.path.splitext(item)
            all_files.append(filename)
        self.all_files = sorted(all_files)
        return self.all_files


def main():
    inputQueue = InputQueue()
    filenames = inputQueue.load_pdf_filenames()
    print('pdf_files:', inputQueue.pdf_files)

if __name__ == "__main__":
    main()