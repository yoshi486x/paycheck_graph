import pprint as pp

from models import full_analyser


def paycheck_analyser():
    """Handles every process of paycheck-graph package."""
    fullAnalyser = full_analyser.FullAnalyzer()
    fullAnalyser.convert_pdf_into_text()
    fullAnalyser.format_text_data_to_analyzable_dict()
    fullAnalyser.paycheck_analysis()
