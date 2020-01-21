import pathlib
import subprocess
import sys


EXEC_DIR = pathlib.Path(sys.exec_prefix)

class PdfReader(object):
    def convert_pdf_to_txt(path):
        """TODO:
        Revise input/output_prefix to not use EXEC_DIR. This only works on my env.
        """
        py_path = EXEC_DIR / "bin" / "pdf2txt.py"
        input_prefix = EXEC_DIR / '..'/'template' / 'input' / 'paycheck'
        output_prefix = EXEC_DIR / '..'
        input_pdf = input_prefix / path
        output_dir = output_prefix / 'output.txt'
        tmp = subprocess.call(['pdf2txt.py', '-V', '-o', str(output_dir), str(input_pdf)])


class TestModules(object):
    """Use this for debugging only."""
    def test1():
        py_path = EXEC_DIR / "bin" / "pdf2txt.py"
        print('Exec: ', EXEC_DIR)
        print('Path: ', py_path)
        # script_dir = '/Users/dev-yoshiki/Hobby/paycheck_reader/paycheck/bin/pdf2txt.py'
        return

if __name__ == "__main__":
    # TestModules.test1()
    with open('model/debug_info.txt', 'r') as txt_file:
        txt_file.seek(1)
        line = txt_file.readline()
        print(line)
        # for row in reader:

    path = line
    PdfReader.convert_pdf_to_txt(path)

