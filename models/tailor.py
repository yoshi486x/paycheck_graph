import collections
import csv
import math
import os
import pathlib
import pprint

try:
    import data_model 
except ModuleNotFoundError:
    from models import data_model

DATA_NAME = 'data'
HOME_PATH = pathlib.Path(os.getcwd())
TEXT_FILE = 'output.txt'
pp = pprint.PrettyPrinter(indent=2)


class PartitionerModel(data_model.DataModel):
    def __init__(self):
        super().__init__()
        self.temp_data = collections.defaultdict(list)
        self.ankers = ['■支給額明細', '■勤怠情報', '■口座情報']
        # self.ankers = ['■支給額明細', '■勤怠情報', '（注）「*」は非課税項目']
        self.ankerIndexes = [] * 5
        self.block1, self.block2, self.block3, self.block4 = [], [], [], []
        self.keys = ['profile', 'summary', 'incomes', 'deductions', 'attendances', 'others']
        self.dict_data = collections.defaultdict(dict, {key:[] for key in self.keys})

        self.profileKeys = ['原籍会社', '社員番号', '氏名', '所属部署']
        self.summaryKeys = ['check_type', '支給年月日', '支給額合計', '控除額合計', '差引支給額']
        self.incomesTitles = ['■支給額明細', '支給項目']
        self.deductionsTitles = ['■控除額明細', '控除項目']
        self.attendancesTitles = ['■勤怠情報', '勤怠管理項目']
        self.othersTitles = ['■その他情報', 'その他']
        self.remainedTitles = ['■口座情報', '振込口座']

    def category_counter(self, block, init_ankers):
        # ankers = ankers[2::]
        print('ankers', init_ankers)
        [print(j, item) for j, item in enumerate(block)]
        print('len', len(block), '\n')

        """remove ankers without ■ in it"""
        selected_ankers = []
        for j, anker in enumerate(init_ankers):
            if list(anker)[0] == '■' and j != 0:
                selected_ankers.append(anker)
        print(selected_ankers)

        """get value on top of selected_anker"""
        bottom_ankers = []
        for anker in selected_ankers:
            tempIndex = block.index(anker)
            bottom_ankers.append(block[tempIndex - 1])
        print(bottom_ankers)

        """remove subtitles from block"""
        [block.remove(anker) for anker in init_ankers]
        [print(j, item) for j, item in enumerate(block)]
        print('len', len(block), '\n')

        """calcurate bottomIndex """
        topIndex = []
        for anker in bottom_ankers:
            topIndex.append(block.index(anker) + 1)
        topIndex.insert(0, 0)
        topIndex.append(len(block))
        print('topIndex', topIndex)

        """calc lengths by ankers"""
        category_lengths = []
        for j, index in enumerate(topIndex):
            try:
                category_lengths.append(abs(index - topIndex[j + 1]))
            except IndexError:
                pass
        print('lengths', category_lengths)

        """calc length of each categories"""
        a, c = tuple(category_lengths)
        b = int((c - a) / 2)

        return (a, b)

    def define_partitions(self):
        # init ankerIndex for start and end
        self.ankerIndexes.append(0)
        for anker in self.ankers:
            self.ankerIndexes.append(self.temp_data[DATA_NAME].index(anker))
        self.ankerIndexes.append(len(self.temp_data[DATA_NAME]))

        print('ankerIndexes', self.ankerIndexes)

    def load_data(self):
        """Load txt data.
        Returns:
            dict: Returns data of dict type.
        """

        text_path = HOME_PATH / TEXT_FILE
        with open(text_path, 'r') as text_file:
            self.temp_data[DATA_NAME] = text_file.read().splitlines()
            # for line in text_file:
            #     if line == '':
            #         continue
            #     self.temp_data[DATA_NAME].append(line.rstrip('\n'))
        while '' in self.temp_data[DATA_NAME]:
            self.temp_data[DATA_NAME].remove('')
        # print('type:', type(self.temp_data[DATA_NAME]))

    def partition_data(self):
        """Partition one list of data into 4 small lists"""
        self.block1 = self.temp_data[DATA_NAME][self.ankerIndexes[0]:self.ankerIndexes[1]]
        self.block2 = self.temp_data[DATA_NAME][self.ankerIndexes[1]:self.ankerIndexes[2]]
        self.block3 = self.temp_data[DATA_NAME][self.ankerIndexes[2]:self.ankerIndexes[3]]
        self.block4 = self.temp_data[DATA_NAME][self.ankerIndexes[3]:self.ankerIndexes[4]]

    def self_correlate_block1(self):
        """Initialization"""
        sec1 = ['check_type']
        sec2 = ['原籍会社', '社員番号', '氏名']
        sec3 = ['所属部署', '支給年月日', '支給額合計', '控除額合計']
        para1, para2, para3 = [], [], []

        """Where function actually begins"""
        para1.append(self.block1[0])
        for sec in sec2:
            index = self.block1.index(sec)
            para2.append(self.block1[index + 3])
        for sec in sec3:
            index = self.block1.index(sec)
            para3.append(self.block1[index + 1])

        # Pickup 所属部署 and combine with profile-info
        para2.append(para3.pop(0))
        sec2.append(sec3.pop(0))

        # Combine check_type with summary-infos
        sec1.extend(sec3)
        para1.extend(para3)

        self.update_datamodel(self.keys[0], sec1, para1)
        self.update_datamodel(self.keys[1], sec2, para2)
         
        """exception for 所属部署 with more than two lines"""
        new_department = []
        startIndex = self.block1.index('所属部署')
        endIndex = self.block1.index('支給年月日') - 1
        lines = abs(endIndex - startIndex)
        # print(lines)

        if  lines > 1:
            for index in startIndex + 1, endIndex:
                new_department.append(self.block1[index])
            self.dict_data['summary']['所属部署'] = ''.join(new_department)

    def self_correlate_block2(self):
        """classify big block into categories"""
        slim_block = self.block2
        length1, length2 = self.category_counter(slim_block, self.incomesTitles + self.deductionsTitles )

        keys1, key2, values1, values2 = [], [], [], []
        AL, OL = length1, length2
        keys1 = slim_block[:AL]
        keys2 = slim_block[AL:AL + OL]
        values1 = slim_block[AL + OL:AL + OL + AL]
        values2 = slim_block[AL + OL + AL:AL + OL + AL + OL]

        """Update dict_data"""
        self.update_datamodel('incomes', keys1, values1)
        self.update_datamodel('deductions', keys2, values2)

    def self_correlate_block3(self):
        def remove_stray_data(mylist):
            """Remove 差引支給額 value"""
            staryIndex = mylist.index(mylist[-1])
            del mylist[staryIndex]
            return mylist

        """classify big block into categories"""
        slim_block = self.block3
        slim_block = remove_stray_data(slim_block)
        length1, length2 = self.category_counter(slim_block, self.attendancesTitles+self.othersTitles)

        """store each categ keys and values in list"""
        keys1, key2, values1, values2 = [], [], [], []
        AL, OL = length1, length2
        keys1 = slim_block[:AL]
        keys2 = slim_block[AL:AL + OL]
        values1 = slim_block[AL + OL:AL + OL + AL]
        values2 = slim_block[AL + OL + AL:AL + OL + AL + OL]

        self.update_datamodel('attendances' , keys1, values1)
        self.update_datamodel('others', keys2, values2)

    def update_datamodel(self, name, keys, values):
        zipped = zip(keys, values)
        self.dict_data[name] = dict(zip(keys, values))
        print('**dict_data updated**')
        return

def main():
    """ Without printing
    partitioner = PartitionerModel()
    partitioner.load_data()
    partitioner.define_partitions()
    partitioner.partition_data()
    partitioner.self_correlate_block1()
    partitioner.self_correlate_block2()
    partitioner.self_correlate_block3()
    """
    partitioner = PartitionerModel()
    partitioner.load_data()
    # pp.pprint(partitioner.temp_data)
    for j, item in enumerate(partitioner.temp_data[DATA_NAME]):
        print(j, item)
    partitioner.define_partitions()

    partitioner.partition_data()
    print('\nblock1:', partitioner.block1)
    print('\nblock2:', partitioner.block2)
    print('\nblock3:', partitioner.block3)
    print('\nblock4:', partitioner.block4)
    print('\n')
    partitioner.self_correlate_block1()
    # pp.pprint(partitioner.dict_data)
    # print('\n')
    partitioner.self_correlate_block2()
    pp.pprint(partitioner.dict_data)
    print('\n')
    partitioner.self_correlate_block3()
    pp.pprint(partitioner.dict_data)
    print('\n')


if __name__ == "__main__":
    main()

class CleanserModel(object):
    
    def employee(self, parameter_list):
        pass
    def employee(self, parameter_list):
        pass
    def employee(self, parameter_list):
        pass
    def employee(self, parameter_list):
        pass