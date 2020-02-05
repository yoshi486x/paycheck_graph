import collections
import csv
import datetime
import math
import os
import pathlib
import pprint as pp
import re

from views import console

TEXT_DIR_PATH = 'data/output/temp'

class DataModel(object):
    """Base model of source data when while being extracted and formatted"""
    def __init__(self, list_data=None, filenames=list):
        self.keys = ['profile', 'summary', 'incomes', 'deductions', 'attendances', 'others']
        self.list_data = list_data
        self.dict_data = collections.defaultdict(dict, {key:[] for key in self.keys})
        self.filenames = filenames


class PartitionerModel(DataModel):
    """TODO Find a way to read multiple data with this model"""
    def __init__(self):
        super().__init__()
        self.ankers = ['■支給額明細', '■勤怠情報', '■口座情報']
        self.ankerIndexes = [] * 5
        self.block1, self.block2, self.block3, self.block4 = list, list, list, list
        self.profileKeys = ['原籍会社', '社員番号', '氏名', '所属部署']
        self.summaryKeys = ['check_type', '支給年月日', '支給額合計', '控除額合計', '差引支給額']
        self.incomesTitles = ['■支給額明細', '支給項目']
        self.deductionsTitles = ['■控除額明細', '控除項目']
        self.attendancesTitles = ['■勤怠情報', '勤怠管理項目']
        self.othersTitles = ['■その他情報', 'その他']
        self.remainedTitles = ['■口座情報', '振込口座']

    def load_data(self, filename):

        """
        :type filename: int
        :stype: dict
        :rtype: 
        """
        suffix = '.txt'
        base_dir = console.get_base_dir_path()
        text_file_path = pathlib.Path(base_dir, TEXT_DIR_PATH, filename).with_suffix(suffix)

        with open(text_file_path, 'r') as text_file:
            list_data = text_file.read().splitlines()
        while '' in list_data:
            list_data.remove('')
        self.list_data = list_data
        return

    def category_counter(self, block, init_ankers):
        # ankers = ankers[2::]
        # print('ankers', init_ankers)
        # [print(j, item) for j, item in enumerate(block)]
        # print('len', len(block), '\n')

        """remove ankers without ■ in it"""
        selected_ankers = []
        for j, anker in enumerate(init_ankers):
            if list(anker)[0] == '■' and j != 0:
                selected_ankers.append(anker)
        # print(selected_ankers)

        """get value on top of selected_anker"""
        bottom_ankers = []
        for anker in selected_ankers:
            tempIndex = block.index(anker)
            bottom_ankers.append(block[tempIndex - 1])
        # print(bottom_ankers)

        """remove subtitles from block"""
        [block.remove(anker) for anker in init_ankers]
        # [print(j, item) for j, item in enumerate(block)]
        # print('len', len(block), '\n')

        """calcurate bottomIndex """
        topIndex = []
        for anker in bottom_ankers:
            topIndex.append(block.index(anker) + 1)
        topIndex.insert(0, 0)
        topIndex.append(len(block))
        # print('topIndex', topIndex)

        """calc lengths by ankers"""
        category_lengths = []
        for j, index in enumerate(topIndex):
            try:
                category_lengths.append(abs(index - topIndex[j + 1]))
            except IndexError:
                pass
        # print('lengths', category_lengths)

        """calc length of each categories"""
        a, c = tuple(category_lengths)
        b = int((c - a) / 2)

        return (a, b)

    def define_partitions(self):
        # init ankerIndex for start and end
        self.ankerIndexes.append(0)
        for anker in self.ankers:
            self.ankerIndexes.append(self.list_data.index(anker))
        self.ankerIndexes.append(len(self.list_data))
        # print('ankerIndexes', self.ankerIndexes)

    def partition_data(self):
        """Partition one list of data into 4 small lists"""
        self.block1 = self.list_data[self.ankerIndexes[0]:self.ankerIndexes[1]]
        self.block2 = self.list_data[self.ankerIndexes[1]:self.ankerIndexes[2]]
        self.block3 = self.list_data[self.ankerIndexes[2]:self.ankerIndexes[3]]
        self.block4 = self.list_data[self.ankerIndexes[3]:self.ankerIndexes[4]]

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
        # print('**dict_data updated**')
        return

    def value_format_date(self):
        thisdate = self.dict_data['profile']['支給年月日']
        self.dict_data['profile']['支給年月日'] = datetime.datetime.strptime(thisdate, '%Y年%m月%d日').strftime('%Y-%m-%d')

    def value_format_deductions(self, category='deductions'):
        for key, value in self.dict_data[category].items():
            self.dict_data[category][key] = -value

    def value_format_digit(self):
        the_data = self.dict_data
        for category in self.keys:
            # pp.pprint(the_data[category])
            for key, value in the_data[category].items():
                # print('value', value)
                if type(value) != (int or float):
                    if value.replace(',', '').isdigit() is True:
                        the_data[category][key] = int(value.replace(',', ''))
                    elif value.replace('.', '').isdigit() is True:
                        the_data[category][key] = float(value)
                """TODO rstrip the check_type and remoe space in between"""
                # if value
        # pp.pprint(the_data)
        # pp.pprint(self.dict_data)

    def value_format_remove_dot_in_keys(self, category='attendances', new_pairs=[], initializer={}):
        """TODO: remove dot from keys"""
        def find_dot_generator():
            for key, value in self.dict_data[category].items():
                yield re.sub('\([^)]*\)', '', key), value
        
        generator = find_dot_generator()
        [new_pairs.append(item) for item in generator]
        self.dict_data[category] = initializer
        self.dict_data[category].update(new_pairs)
        # pp.pprint(self.dict_data)


def main():
    partitioner = PartitionerModel()
    # pp.pprint(partitioner.temp_data)
    for j, item in enumerate(partitioner.list_data):
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
    # pp.pprint(partitioner.dict_data)
    # print('\n')
    partitioner.value_format_digit()
    partitioner.value_format_date()
    partitioner.value_format_deductions()
    partitioner.value_format_remove_dot_in_keys()
    pp.pprint(partitioner.dict_data)
    print('\n')


if __name__ == "__main__":
    main()