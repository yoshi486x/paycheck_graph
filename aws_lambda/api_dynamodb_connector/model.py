import collections
import json
import numpy as np
import pandas as pd

def create_dataframe(*args):

    items = args
    for item in items:
        dates, keys, values, indexes = [], [], [], []

        dates, keys, values = [], [], []
        date = dict_data[PAID_DATE]
        for key, value in dict_data['incomes'].items():
            values.append(value)
            keys.append(key)
            dates.append(date)
        df = pd.DataFrame({'date': dates, 'type': keys, 'income': values})
        dataframes.append(df)

    # Combine tables of each json file
    df = pd.concat(dataframes)
    df = df.pivot(index='date', columns='type', values='income')

    self.dataframe = df