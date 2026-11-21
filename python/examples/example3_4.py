"""Port of ``example3_4.m``: the Sharpe ratio of the IGE ETF.

The book says the output should be 0.7893.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.matlab_compat import excel_serial_to_yyyymmdd, sort_index, xlsread
from epchan.paths import data_path


def main():
    num, _txt = xlsread(data_path("IGE.xls"))

    tday = np.array([excel_serial_to_yyyymmdd(v) for v in num[:, 0]])
    cls = num[:, -1]  # the last column contains the adjusted close prices.

    _sorted_tday, sort_index_ = sort_index(tday)  # sort tday into ascending order.
    cls = cls[sort_index_]  # sort cls into ascending order of dates.

    dailyret = (cls[1:] - cls[:-1]) / cls[:-1]  # daily returns

    # excess daily returns = strategy returns - financing cost, assuming a
    # risk-free rate of 4% per annum and 252 trading days in a year
    excess_ret = dailyret - 0.04 / 252

    sharpe_ratio = np.sqrt(252) * excess_ret.mean() / excess_ret.std()
    print("sharpeRatio = %.4f   (the book says 0.7893)" % sharpe_ratio)
    return sharpe_ratio


if __name__ == "__main__":
    main()
