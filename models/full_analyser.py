"""Define full-analyser model"""
import pprint as pp

from models import pdf_reader
from models import recording
from models import tailor

class FullDataModel(object):
    def __init__(self, data=list):
        self.data = data

class FullAnalyzer(object):
    """Handle data model on anylysing process
    Steps:
    1. Get all pdf file name for paycheck
    2. for each file, proceed Extract and Transform
    """
    def __init__(self, filenames=None):
        self.filenames = filenames

    def convert_pdf_into_text(self):
        pdfReader = pdf_reader.PdfReader()
        pdfReader.load_pdf_filenames()
        self.filenames = sorted(pdfReader.filenames)
        for filename in self.filenames:
            pdfReader.convert_pdf_to_txt(filename)

    def format_text_data_to_analyzable_dict(self):
        """Create instance for Recording models (MongoDB)"""
        # recording_model = recording.RecordingModel(self.filenames)

        """Parameter tuning for debuging use"""
        # filenames = self.filenames[1:2]
        filenames = self.filenames

        """Main analyse model"""
        for filename in filenames:
            recording_model = recording.RecordingModel(filename)
            """Extract and Transform text data
            output: MongoDB, data/output/json
            """
            text_tailor = tailor.PartitionerModel()
            text_tailor.load_data(filename)
            text_tailor.value_format_digit()
            text_tailor.define_partitions()
            text_tailor.partition_data()
            text_tailor.self_correlate_block1()
            text_tailor.self_correlate_block2()
            text_tailor.value_format_date()
            text_tailor.value_format_deductions()
            text_tailor.value_format_remove_dot_in_keys()
            # pp.pprint(text_tailor.dict_data)

            # Register data to db and json. Order must be json to db to avoid erro 
            print("@@@@@@@@@@@@Export@@@@@@@@@@@@@@@\n")
            recording_model.record_data_in_json(text_tailor.dict_data)
            recording_model.record_data_to_mongo(text_tailor.dict_data)

    def paycheck_analysis(self):
        pass

