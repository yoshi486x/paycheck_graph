import collections


DATA_NAME = 'data'


class DataModel(object):
    """Base model of source data when while being extracted and formatted"""
    def __init__(self):
        self.data = collections.defaultdict(str)
        self.employee = collections.defaultdict(str)
        self.summary = collections.defaultdict(str)
        self.incomes = collections.defaultdict(str)
        self.deductions = collections.defaultdict(str)
        self.attendances = collections.defaultdict(str)
        self.others = collections.defaultdict(str)

    def init_data(self, name=DATA_NAME):
        # self.data = list([collections.defaultdict(str)])
        self.data[name] = [self.employee, self.summary, self.incomes, self.deductions, self.attendances, self.others]