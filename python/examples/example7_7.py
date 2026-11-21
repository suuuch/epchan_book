"""Port of ``example7_7.m``: a monthly decile reversal strategy on the SP500.

The book says the output should be

    Avg ann return=-0.9167 Sharpe ratio=-0.1055
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from scipy.io import loadmat

from epchan.backshift import backshift
from epchan.is_last_trading_day_of_month import is_last_trading_day_of_month
from epchan.lag1 import lag1
from epchan.paths import data_path
from epchan.smartmean import smartmean
from epchan.smartstd import smartstd
from epchan.smartsum import smartsum


def main():
    mat = loadmat(data_path("SPX_20071123.mat"))
    tday = mat["tday"].ravel()
    cl = mat["cl"]

    # find the indices of the days that are at month ends.
    month_ends = np.flatnonzero(is_last_trading_day_of_month(tday))

    monthly_ret = ((cl[month_ends, :] - lag1(cl[month_ends, :]))
                   / lag1(cl[month_ends, :]))

    # The MATLAB original also builds ``mycl = fillMissingData(cl)`` for a
    # commented-out alternative computation; it is not needed here.

    # sort stocks by monthly returns in ascending order
    monthly_ret_sorted = np.sort(monthly_ret, axis=1, kind="stable")
    sort_index = np.argsort(monthly_ret, axis=1, kind="stable")

    # these are the sorted monthly returns of the previous year
    prev_year_monthly_ret_sorted = backshift(12, monthly_ret_sorted)
    # the sort index of the previous year
    prev_year_sort_index = backshift(12, sort_index)

    positions = np.zeros_like(monthly_ret)

    for m in range(12, monthly_ret.shape[0]):
        has_returns = (np.isfinite(prev_year_monthly_ret_sorted[m, :])
                       & np.isfinite(cl[month_ends[m - 1], :]))
        my_sort_index = prev_year_sort_index[m, has_returns].astype(int)

        # take top decile of stocks as longs, bottom decile as shorts
        topn = len(my_sort_index) // 10
        if topn == 0:
            continue

        positions[m - 1, my_sort_index[:topn]] = -1
        positions[m - 1, my_sort_index[-topn:]] = 1

    ret = smartsum(lag1(positions) * monthly_ret, axis=1)

    avgannret = 12 * smartmean(ret, axis=0)
    sharpe = np.sqrt(12) * smartmean(ret, axis=0) / smartstd(ret, axis=0)

    print("Avg ann return=%7.4f Sharpe ratio=%7.4f" % (avgannret, sharpe))


if __name__ == "__main__":
    main()
