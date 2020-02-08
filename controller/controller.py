import pprint as pp

from models import full_analyser


def paycheck_analyser():
    """Handles every process of paycheck-graph package."""
    fullAnalyser = full_analyser.FullAnalyser()
    # fullAnalyser.ask_for_db_activation()
    # fullAnalyser.convert_pdf_into_text()
    # fullAnalyser.format_text_data_to_analysable_dict()
    fullAnalyser.visualize_in_graph()
