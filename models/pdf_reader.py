import csv
import os
import pathlib
import subprocess
import sys

EXEC_CMD = 'pdf2txt.py'
OUTPUT_DIR_PATH = 'data/output/temp'
PDF_DIR_PATH = 'data/pdf'
PDF_FILENAME_NAME = 'FILENAME'


class PdfModel(object):
    def __init__(self, filenames):
        self.filenames = filenames

class PdfReader(PdfModel):
    def __init__(self, filenames=None, base_dir=None):
        super().__init__(filenames=filenames)
        if not base_dir:
            base_dir = self.get_base_dir_path()
        self.base_dir = base_dir

    def convert_pdf_to_txt(self, filename):
        """
        :type filename: int
        :rtype: 
        """

        """Organize input path info"""
        suffix = '.pdf'
        input_full_dir_path = pathlib.Path(self.base_dir, PDF_DIR_PATH)
        input_pdf = pathlib.Path(input_full_dir_path, filename).with_suffix(suffix)

        """Organize output path info"""
        suffix = '.txt'
        output_full_dir_path = pathlib.Path(self.base_dir, OUTPUT_DIR_PATH)
        output_filename, _ = os.path.splitext(filename)
        output_file_path = pathlib.Path(output_full_dir_path, output_filename).with_suffix(suffix)

        """Call pdf2text.py"""
        subprocess.call([EXEC_CMD, '-V', '-o', str(output_file_path), str(input_pdf)])
    
    def get_base_dir_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def load_pdf_filenames(self, filenames=list):

        filenames = []
        pdf_full_dir_path = pathlib.Path(self.base_dir, PDF_DIR_PATH)
        for item in os.listdir(pdf_full_dir_path):
            filename, _ = os.path.splitext(item)
            filenames.append(filename)
        self.filenames = filenames
        return

def main():
    reader = PdfReader()
    reader.load_pdf_filenames()


if __name__ == "__main__":
    main()