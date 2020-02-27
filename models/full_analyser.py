"""Define full-analyser model"""
import pprint as pp

from models import pdf_reader, recording, tailor, visualizing
from views import console

class FullDataModel(object):
    def __init__(self, data=list):
        self.data = data

class FullAnalyser(object):
    """Handle data model on anylysing process
    Steps:
    1. Get all pdf file name for paycheck
    2. for each file, proceed Extract and Transform
    """
    def __init__(self, db='MongoDB', filenames=None, speak_color='green', status=None):
        self.db = db
        self.filenames = filenames
        self.speak_color = speak_color
        self.status = status

    def ask_for_db_activation(self):
        while True:
            # template = console.get_template('hello.txt', self.speak_color)
            template = console.get_template('db_activation.txt', self.speak_color)
            is_yes = input(template.substitute({
                'db': self.db}))

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                self.status = True
                break

            if is_yes.lower() == 'n' or is_yes.lower() == 'no':
                self.status = False
                break

    def convert_pdf_into_text(self):
        pdfReader = pdf_reader.PdfReader()
        pdfReader.load_pdf_filenames()
        self.filenames = sorted(pdfReader.filenames)
        for filename in self.filenames:
            pdfReader.convert_pdf_to_txt(filename)

    def format_text_data_to_analysable_dict(self):
        """Create instance for Recording models (MongoDB)"""
        mongo_model = recording.MongoModel(None)
        if not mongo_model.get_mongo_profile():
            print('{} seems to be not running.'.format(self.db))
            self.status = False
        else:
            self.status = True

        """Parameter tuning for debuging use"""
        # filenames = self.filenames[1:2]
        filenames = self.filenames

        """Main analyse model"""
        for filename in filenames:
            """Extract and Transform text data
            output: MongoDB, data/output/json
            """
            # Transform text data into dict format
            text_tailor = tailor.PartitionerModel()
            text_tailor.load_data(filename)
            text_tailor.value_format_digit()
            text_tailor.define_partitions()
            text_tailor.partition_data()
            text_tailor.self_correlate_block1()
            # pp.pprint(text_tailor.dict_data)
            text_tailor.self_correlate_block2()
            text_tailor.value_format_date()
            text_tailor.value_format_deductions()
            text_tailor.value_format_remove_dot_in_keys()

            # Register data to db and json. Order must be json to db to avoid erro 
            recording_model = recording.RecordingModel(filename, self.status)
            recording_model.record_data_in_json(text_tailor.dict_data)
            if self.status:
                recording_model.record_data_to_mongo(text_tailor.dict_data)

    def visualize_income_timechart(self):
        """TODO: import and modify this func to enable walkthrough
        Add demo dir """

        visual = visualizing.VisualizingModel(None)
        visual.create_base_table()
        visual.sort_table()
        visual.save_graph_to_image()

