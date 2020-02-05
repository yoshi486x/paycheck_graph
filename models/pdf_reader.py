import csv
import os
import pathlib
import pprint as pp
import subprocess
import sys

from views import console

EXEC_CMD = 'pdf2txt.py'
OUTPUT_DIR_PATH = 'data/output/temp'
PDF_DIR_PATH = 'data/pdf'
PDF_FILENAME_NAME = 'FILENAME'


class PdfModel(object):
    def __init__(self, filenames):
        self.filenames = filenames

class PdfReader(PdfModel):
    def __init__(self, filenames=None):
        super().__init__(filenames=filenames)

    def convert_pdf_to_txt(self, filename):
        """
        :type filename: int
        :rtype: 
        """

        """Organize input path info"""
        suffix = '.pdf'
        base_path = console.get_base_dir_path()
        input_full_dir_path = pathlib.Path(base_path, PDF_DIR_PATH)
        input_pdf = pathlib.Path(input_full_dir_path, filename).with_suffix(suffix)

        """Organize output path info"""
        suffix = '.txt'
        output_full_dir_path = pathlib.Path(base_path, OUTPUT_DIR_PATH)
        output_filename, _ = os.path.splitext(filename)
        output_file_path = pathlib.Path(output_full_dir_path, output_filename).with_suffix(suffix)

        """Call pdf2text.py"""
        subprocess.call([EXEC_CMD, '-V', '-o', str(output_file_path), str(input_pdf)])

    def load_pdf_filenames(self, filenames=list):

        filenames = []
        base_path = console.get_base_dir_path()
        pdf_full_dir_path = pathlib.Path(base_path, PDF_DIR_PATH)
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