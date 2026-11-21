"""Port of ``example3_4a.m``: IGE against SPY, a market neutral strategy.

The book says the Sharpe ratio should be 0.7618 for IGE alone and 0.7837 for
the market neutral portfolio.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.matlab_compat import excel_serial_to_yyyymmdd, sort_index, xlsread
from epchan.paths import data_path


def _read_adjusted_close(filename):
    """Read a spreadsheet and return the adjusted close prices sorted by date."""
    num, _txt = xlsread(filename)
    tday = np.array([excel_serial_to_yyyymmdd(v) for v in num[:, 0]])
    cls = num[:, -1]
    _sorted_tday, sort_index_ = sort_index(tday)
    return cls[sort_index_]


def main():
    cls = _read_adjusted_close(data_path("IGE.xls"))

    dailyret = (cls[1:] - cls[:-1]) / cls[:-1]
    excess_ret = dailyret - 0.04 / 252
    sharpe_ratio = np.sqrt(252) * excess_ret.mean() / excess_ret.std()
    print("sharpeRatio (IGE)        = %.4f   (the book says 0.7618)" % sharpe_ratio)

    cls = _read_adjusted_close(data_path("SPY.xls"))
    dailyret_spy = (cls[1:] - cls[:-1]) / cls[:-1]

    # net daily returns (divide by 2 because we now have twice as much capital)
    net_ret = (dailyret - dailyret_spy) / 2
    sharpe_ratio = np.sqrt(252) * net_ret.mean() / net_ret.std()
    print("sharpeRatio (IGE vs SPY) = %.4f   (the book says 0.7837)" % sharpe_ratio)
    return sharpe_ratio


if __name__ == "__main__":
    main()
