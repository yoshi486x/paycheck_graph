import collections
import csv
import datetime
# import numpy as np
import os
import pathlib
import string
import subprocess
import sys

TEXT_FILE_NAME = 'output.txt'
HOME_PATH = pathlib.Path(os.getcwd())
EMPLOYEE_INFO_INDEX_DELTA = 6   # 3 * 2

class CsvModel(object):
    def __init__(self, csv_file):
        self.csv_file = csv_file
        if not os.path.exists(csv_file):
            pathlib.Path(csv_file).touch()

class Extractor(object):
    """Extract necessary info from textfile to csv files."""
    # def __init__(self, csv_file=None):
    #     if not csv_file:
    #         csv_file = self.get_csv_file_path()

    def extract_text():
        txt_file_path = HOME_PATH / TEXT_FILE_NAME
        # with open(str(Extractor.get_txt_file_path())) as f:
        with open(txt_file_path) as f:
            # t = string.Template(f.read())
            """Read whole and convert into list"""
            mylist = f.read().splitlines()
            print(mylist)
        return mylist
    
    def make_tuple_pairs(mylist):
        """employee_info
        1. Define dict.
        2. Find index of each keys.
        3. Insert value to dict.
        """
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
        #1.
        incomeDetails = mylist.index('■支給額明細')
        deductionDetails = mylist.index('■控除額明細')
        attendanceDetails = mylist.index('■勤怠情報')
        otherDetails = mylist.index('■その他情報')
        income_columns, deduction_columns, attendance_columns, other_columns = [], [], [], []

        indexes = [incomeDetails, deductionDetails, attendanceDetails, otherDetails]
        columns = [income_columns, deduction_columns, attendance_columns, other_columns]
        
        # print('indexes:', indexes)
        # print('columns:', columns)

        # 2.
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
        return employee_info, general_info, incomes, deductions, attendances, others


        

    def get_txt_file_path():
        txt_file_path = os.getcwd() / TEXT_FILE_NAME
        return txt_file_path

if __name__ == "__main__":
    CsvModel('gross_income.csv')
    CsvModel('total_deduction.csv')

    payment_list = Extractor.extract_text()
    print('\n\n++++++++++++++++++++++++++\n\n')
    extracted_items = Extractor.make_tuple_pairs(payment_list)
    print('\n\n++++++++++++++++++++++++++\n\n')
    for item in extracted_items:
        print(item)
        print('\n\n')
