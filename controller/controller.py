from models import info_extractor
from models import pdf_reader

def paycheck_analyser():
    """TODO: 
    1. Object orient the extractor function (forget about reader right now)>>Done
    2. Make extractor function callable from controller.>>Done
    3. Make visualizer function callable from controller.
    4. Enable extractor to handle 'the' spacing issue.
    5. Enable reader to read multiple pdfs.
    6. Enable all models to handle multiple pdfs.
    """
    # pdf_reader = pdf_reader.PdfReader()
    # pdf_reader.convert_pdf_to_txt()
    extractor = info_extractor.Extractor()
    extractor.extract_text()
    print('extractor.data:', extractor.data)
    extractor.make_tuple_pairs()
    print('extractor.data:', extractor.data)
    extractor.dict2json_file()

    """Organize data in analyzable format"""
    formatter = info_extractor.Formatter()
    formatter.load_json_as_dict()
    formatter.format_from_data()
    formatter.dict2json_file()