import collections
import csv
import datetime
import json
import os
import pathlib
import string
import subprocess
import sys

try:
    from models import data_model
except ModuleNotFoundError:
    import data_model

EMPLOYEE_INFO_INDEX_DELTA = 6   # 3 * 2
DATA_NAME = 'data'
HOME_PATH = pathlib.Path(os.getcwd())
TEXT_FILE_NAME = 'output.txt'


class Extractor(data_model.DataModel):
    """Extract necessary info from textfile to csv files."""
    def __init__(self, name='data'):
        super().__init__()
        self.init_data()
        # self.init_data(list)

    def dict2json_file(self, datasource='data.json'):
        """TODO:(yoshiki-11) Import from views module"""
        data_json = json.dumps(self.data, ensure_ascii=False, indent=4)
        data_path = HOME_PATH / datasource
        with open(data_path, 'w') as json_file:
            json_file.write(data_json)
    
    def extract_text(self):
        txt_file_path = HOME_PATH / TEXT_FILE_NAME
        with open(txt_file_path) as f:
            """Read whole and convert into list"""
            self.data[DATA_NAME] = f.read().splitlines()
    
    def make_tuple_pairs(self):
        """employee_info
        1. Define dict.
        2. Find index of each keys.
        3. Insert value to dict.
        """
        mylist=self.data[DATA_NAME]
        # 1. Define dict.
        employee_info = {'原籍会社': None, '社員番号': None, '氏名': None, '所属部署': None}

        # 2. Find index of each keys.
        companyIndex = mylist.index('原籍会社')
        employeeIdIndex = mylist.index('社員番号')
        fullnameIndex = mylist.index('氏名')
        departmentIndex = mylist.index('所属部署')

        # 3. Insert value to dict.
        employee_info['原籍会社'] = mylist[companyIndex + EMPLOYEE_INFO_INDEX_DELTA] 
        employee_info['社員番号'] = mylist[employeeIdIndex + EMPLOYEE_INFO_INDEX_DELTA] 
        employee_info['氏名'] = mylist[fullnameIndex + EMPLOYEE_INFO_INDEX_DELTA] 
        print('employee_info:', employee_info)
        print('\n\n@@@@@@@@@@@@@@@@@@@@\n\n')

        """employee_info2"""
        if mylist[departmentIndex + 3] is not '':
            my_department = mylist[departmentIndex + 2] + mylist[departmentIndex + 3]
        else:
            my_department = mylist[departmentIndex + 2]

        employee_info['所属部署'] = my_department
        print('my_department:', my_department)
        print('employee_info:', employee_info)
        print('\n\n@@@@@@@@@@@@@@@@@@@@\n\n')

        """Detailed informations"""
        general_info = {'paycheck_type': None, '支給年月日': None, '支給額合計': None, '控除額合計': None, '差引支給額': None}
        general_info['paycheck_type'] = mylist[0].replace(' ', '')
        paidDate = mylist.index('支給年月日')
        grossIncome = mylist.index('支給額合計')
        totalDeduction = mylist.index('控除額合計')

        general_info['支給年月日'] = mylist[paidDate + 2]
        general_info['支給年月日'] = datetime.datetime.strptime(general_info['支給年月日'], '%Y年%m月%d日').strftime('%Y-%m-%d')
        general_info['支給額合計'] = int(mylist[grossIncome + 2].replace(',', ''))
        general_info['控除額合計'] = int(mylist[totalDeduction + 2].replace(',', ''))
        general_info['差引支給額'] = general_info['支給額合計'] - general_info['控除額合計']

        print('general_info:', general_info)
        print('\n\n@@@@@@@@@@@@@@@@@@@@\n\n')

        """Details' tables
        1. Find index of each subtitles
        2. Find next '' in mylist
        3. Count numbers for each columns
        4. Calc 'delta' amount for each subtitles
        5. Save amounts for each columns
        """
        #1. Find index of each subtitles
        incomeDetails = mylist.index('■支給額明細')
        deductionDetails = mylist.index('■控除額明細')
        attendanceDetails = mylist.index('■勤怠情報')
        otherDetails = mylist.index('■その他情報')
        income_columns, deduction_columns, attendance_columns, other_columns = [], [], [], []

        indexes = [incomeDetails, deductionDetails, attendanceDetails, otherDetails]
        columns = [income_columns, deduction_columns, attendance_columns, other_columns]
        # print('indexes:', indexes, 'columns:', columns)

        # 2. Find next '' in mylist
        for index, column in zip(indexes, columns) :
            # print('index:', index, 'column:', column)
            index += 2  # delta value for being at left row. They include two extra strings.
            while mylist[index] is not '':
                """TODO: Revise the condition of while loop to adjust '' in between list"""
                # print('key:', mylist[index])
                column.append(mylist[index])
                index += 1
                # print('index:', index)

        print('indexes:', indexes)
        print('columns:', columns)

        #3. Count numbers for each columns
        column_lens = [0] * len(indexes)
        for i, column in enumerate(columns):
            column_lens[i] = len(column)
        # print('\n\n', 'column_lens:', column_lens)

        #4. Calc 'delta' amount for each subtitles
        incomeAmounts = deductionDetails + 2 + column_lens[1] + 1
        deductionAmounts = incomeAmounts + column_lens[0] + 1
        print(incomeAmounts, mylist[incomeAmounts])
        print(deductionAmounts, mylist[deductionAmounts])

        attendanceAmounts = otherDetails + 2 + column_lens[3] + 1
        otherAmounts = attendanceAmounts + column_lens[2] + 1 + 2
        print(attendanceAmounts, mylist[attendanceAmounts])
        print(otherAmounts, mylist[otherAmounts])

        #5. Save amounts for each columns
        indexesAmounts = [incomeAmounts, deductionAmounts, attendanceAmounts, otherAmounts]
        income_amounts, deduction_amounts, attendance_amounts, other_amounts = [], [], [], []
        item_amounts = [income_amounts, deduction_amounts, attendance_amounts, other_amounts]

        for index, item, length in zip(indexesAmounts, item_amounts, column_lens):
            while length != 0:
                item.append(mylist[index])
                index += 1
                length -= 1

        print('item_amounts:', item_amounts)
        print('\n\n@@@@@@@@@@@@@@@@@@@@\n\n')

        #6. Create dict from two lists.
        """Create list of dicts by for-zip loop: FAILED at the moment"""
        # for detail, column, amount in zip(details_dicts, columns, item_amounts):
        #     print('column:', column, '\n', 'amount:', amount)
        #     detail = dict(zip(column, amount))

        # incomes, deductions, attendances, others = dict(), dict(), dict(), dict()
        incomes = dict(zip(income_columns, income_amounts))
        deductions = dict(zip(deduction_columns, deduction_amounts))
        attendances = dict(zip(attendance_columns, attendance_amounts))
        others = dict(zip(other_columns, other_amounts))
        # details_dicts = [incomes, deductions, attendances, others]
        # print(details_dicts)
        # return employee_info, general_info, details_dicts

        """Added while refactoring to OOM"""
        self.employee = employee_info
        self.summary = general_info
        self.incomes = incomes
        self.deductions = deductions
        self.attendances = attendances
        self.others = others
        # self.data = (self.employee, self.summary, self.incomes, self.deductions, self.attendances, self.others)
        self.init_data()
        self.dict2json_file()

        return employee_info, general_info, incomes, deductions, attendances, others

    def get_txt_file_path():
        txt_file_path = os.getcwd() / TEXT_FILE_NAME
        return txt_file_path


class DebugModule(object):
    def main2():
        extractor = Extractor()
        extractor.extract_text()
        print('extractor.data:', extractor.data)
        extractor.make_tuple_pairs()
        print('extractor.data:', extractor.data)
        extractor.dict2json_file()

        formatter = Formatter()
        formatter.load_json_as_dict()
        formatter.format_from_data()
        formatter.dict2json_file()
        # DebugModule.print_extracted_items(*formatter.data)

    def print_extracted_items(*args):
        for arg in args:
            print(arg, '\n')

if __name__ == "__main__":
    # DebugModule.main()
    DebugModule.main2()
