"""This script is not complete and has not been implemented in 
remote repo.
TODO: Create scoring sheet for income table to have its columns ordered
in better understandable way. """

import collections
import math
import numpy as np
import pandas as pd

import pprint
pp = pprint.PrettyPrinter(indent = 2)

def score_variance(mydict):

    """Setup to analysable data structure"""
    cols = []
    variances = []
    for key, val in mydict.items():
        var = val['var']
        cols.append(key)
        variances.append(var)
    variances = np.array(variances)

    # print(cols)
    # print(variances)

    """Calc deviations for each vars"""
    perfect = 100
    deviations = []

    sum = variances.sum()
    adjusted_vars = map(lambda x: int(x/sum)*perfect, variances)
    adjusted_vars = list(map(lambda x: abs(x - perfect), adjusted_vars))

    """Format calculated data for returning value"""
    mydict = dict(zip(cols, adjusted_vars))
    # Check

    # adjusted_vars = np.array(adjusted_vars)
    # [print(i, type(i)) for i in adjusted_vars]

    # myarray = np.vstack((np.array(cols), np.array(adjusted_vars, dtype=int)))
    # myarray = np.vstack((np.array(cols), adjusted_vars))
    # [print(i, type(i)) for i in myarray[1]]
    # new_col = np.array(adjusted_vars).T
    df = pd.DataFrame({'varScore': np.array(adjusted_vars).T}, index=cols)
    print(df)
    

    return 



def main():
    idx = ['over work', 'smart&fun', 'support']
    cols = ['avg', 'var', 'std']
    avgs = [51649, 10000, 25000]
    vars = [189623767, 0, 0]
    stds = [13770, 0, 0]
    df = pd.DataFrame(
                {'avg': avgs,
                'var': vars,
                'std': stds},
                index = idx)
    # print(df)

    data = {
        'over work': {
            'avg': 51649,
            'std': 13770,
            'var': 189623767
            },
        'smart&fun': {
            'avg': 10000,
            'std': 0,
            'var': 0
            },
        'support': {
            'avg': 25000,
            'std': 0,
            'var': 0
            }}
    mydict = collections.defaultdict(dict)
    mydict.update(data)

    scored_vars = score_variance(mydict)
    # if k, v in score_variance.items():


if __name__ == "__main__":
    main()