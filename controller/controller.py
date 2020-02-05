import pprint as pp

from models import full_analyzer


def paycheck_analyser():
    """TODO(yoshiki-11)
    1. Object orient the extractor function (forget about reader right now)>>Done
    2. Make extractor function callable from controller.>>Done
    3. Make visualizer function callable from controller. >>Done
    4. Enable extractor to handle 'the' spacing issue. >>Done
    5. TODO: Export dict to CSV.
    6. Enable reader to read multiple pdfs.
    7. Enable all models to handle multiple pdfs.
    """

    fullAnalyzer = full_analyzer.FullAnalyzer()
    fullAnalyzer.convert_pdf_into_text()
    fullAnalyzer.format_text_data_to_analyzable_dict()
