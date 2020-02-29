import pprint as pp

from models import paycheck_analyzer


def paycheck_analysis():
    """Handles every process of paycheck-graph package."""
    full_analyzer = paycheck_analyzer.AnalyzerModel()
    full_analyzer.ask_for_db_activation()
    full_analyzer.convert_pdf_into_text()
    full_analyzer.format_text_data_to_analysable_dict()
    full_analyzer.visualize_income_timechart()
