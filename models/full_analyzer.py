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
    3. 
    """
    def __init__(self, filenames=None):
        self.filenames = filenames

    def convert_pdf_into_text(self):
        pdfReader = pdf_reader.PdfReader()
        pdfReader.load_pdf_filenames()
        self.filenames = sorted(pdfReader.filenames)
        # self.filenames = pdfReader.filenames
        for filename in self.filenames:
            pdfReader.convert_pdf_to_txt(filename)

    def format_text_data_to_analyzable_dict(self):
        """Create instance for Recording models (MongoDB)"""
        # text_tailor = tailor.PartitionerModel()
        recording_model = recording.RecordingModel()

        """Parameter tuning for debuging use"""
        print("####################\n")
        print('List of loaded pdf filenames')
        pp.pprint(self.filenames)
        print("####################\n")
        filenames = self.filenames[4:6]
        # filenames = self.filenames
        print('Given list parameters')
        pp.pprint(filenames)
        print("####################\n")

        """Main analyse model"""
        for filename in filenames:
            print("+++++++++++++++++++++++++")
            text_tailor = tailor.PartitionerModel()
            """Extract and Transform text data
            Returns: dict
            """       
            text_tailor.load_data(filename)
            text_tailor.define_partitions()
            text_tailor.partition_data()
            text_tailor.self_correlate_block1()
            text_tailor.self_correlate_block2()
            text_tailor.self_correlate_block3()
            text_tailor.value_format_date()
            text_tailor.value_format_digit()
            text_tailor.value_format_deductions()
            text_tailor.value_format_remove_dot_in_keys()
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
            pp.pprint(text_tailor.dict_data)

            """Register data to db """
            print("@@@@@@@@@@@@Mongo@@@@@@@@@@@@@@@\n")
            # recording_model = recording.RecordingModel()
            recording_model.injest_data_to_mongo(text_tailor.dict_data)


