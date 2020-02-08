import collections
import matplotlib

try:
    import info_extractor as ex
except ModuleNotFoundError:
    pass


class Visualizer(object):
    """Base visualizer model"""
    def __init__(self, *args):
        self.data = args

class PaycheckVisualizer(Visualizer):
    """Class to handle visal operation dedicated to paychecks"""
    def __init__(self, *args):
        super().__init__(*args)
        self.employee = collections.defaultdict()
        self.summary = collections.defaultdict()
        self.incomes = collections.defaultdict()
        self.deductions = collections.defaultdict()
        self.attendances = collections.defaultdict()
        self.others = collections.defaultdict()

    def comparting_generator(*args):
        for arg in args:
            yield arg

    def compart_data(self):
        g = self.comparting_generator(*self.data)
        next(g)
        self.employee = next(g)
        self.summary = next(g)
        self.incomes = next(g)
        self.deductions = next(g)
        self.attendances = next(g)
        self.others = next(g)
    
    """TODO(ynakagawa) Create graph using data from all dates"""

        
class Main(object):
    def main():
        data = ex.DebugModule.main()
        print('\n=================visualizer===================\n')
        # data = Main.get_data_from_txt()
        # print('type:', type(data), '\n')
        paycheck_visualiser = PaycheckVisualizer(*data)
        # print(paycheck_visualiser.data, '\n')
        paycheck_visualiser.compart_data()
        print('employee:', paycheck_visualiser.employee, '\n')
        print('summary:', paycheck_visualiser.summary, '\n')
        print('incomes:', paycheck_visualiser.incomes, '\n')
        print('deductions:', paycheck_visualiser.deductions, '\n')
        print('attendances:', paycheck_visualiser.attendances, '\n')
        print('others:', paycheck_visualiser.others, '\n')
        print('\n=================visualizer===================\n')

    
    # def get_data_from_txt():
    #     with open('models/debug_info.txt') as f:
    #         f.readline()
    #         reader = f.readline()   # Read the second line.
    #         # print(reader)
    #     return reader


if __name__ == "__main__":
    Main.main()