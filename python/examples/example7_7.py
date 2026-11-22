"""Port of ``example7_7.m``: a monthly decile reversal strategy on the SP500.

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com
编写者：Ernest Chan
《Quantitative Trading: How to Start Your Own Algorithmic Trading Business》
一书的作者。

The book says the output should be

    Avg ann return=-0.9167 Sharpe ratio=-0.1055

书中给出的输出应为

    年化平均收益率=-0.9167 夏普比率=-0.1055
"""

import sys
from pathlib import Path

# Add this folder to the Python path, just like the MATLAB original adds this
# folder and the data folder to the MATLAB path.
# 将本文件夹添加到 Python 路径中，就像 MATLAB 原版把本文件夹和数据文件夹
# 添加到 MATLAB 路径中那样。
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
    # 查找处于月末的交易日索引。
    month_ends = np.flatnonzero(is_last_trading_day_of_month(tday))

    monthly_ret = ((cl[month_ends, :] - lag1(cl[month_ends, :]))
                   / lag1(cl[month_ends, :]))

    # The MATLAB original also builds ``mycl = fillMissingData(cl)`` for a
    # commented-out alternative computation; it is not needed here.
    # MATLAB 原版还构建了 ``mycl = fillMissingData(cl)``，用于下面被注释掉的
    # 另一种计算方式；此处并不需要。

    # myMonthlyRet=(mycl(monthEnds, :)-lag1(mycl(monthEnds, :)))
    #     ./lag1(mycl(monthEnds, :));
    # 用 mycl 计算月度收益率: myMonthlyRet=(mycl(monthEnds, :)
    #     -lag1(mycl(monthEnds, :)))./lag1(mycl(monthEnds, :));

    # sort stocks by monthly returns in ascending order
    # 按月度收益率升序对股票排序
    monthly_ret_sorted = np.sort(monthly_ret, axis=1, kind="stable")
    sort_index = np.argsort(monthly_ret, axis=1, kind="stable")

    # these are the sorted monthly returns of the previous year
    # 上一年度排序后的月度收益率
    prev_year_monthly_ret_sorted = backshift(12, monthly_ret_sorted)
    # the sort index of the previous year
    # 上一年度的排序索引
    prev_year_sort_index = backshift(12, sort_index)

    positions = np.zeros_like(monthly_ret)

    for m in range(12, monthly_ret.shape[0]):
        has_returns = (np.isfinite(prev_year_monthly_ret_sorted[m, :])
                       & np.isfinite(cl[month_ends[m - 1], :]))
        my_sort_index = prev_year_sort_index[m, has_returns].astype(int)

        # take top decile of stocks as longs, bottom decile as shorts
        # 取最高的十分之一股票做多，最低的十分之一股票做空
        topn = len(my_sort_index) // 10
        if topn == 0:
            continue

        positions[m - 1, my_sort_index[:topn]] = -1
        positions[m - 1, my_sort_index[-topn:]] = 1

    ret = smartsum(lag1(positions) * monthly_ret, axis=1)

    avgannret = 12 * smartmean(ret, axis=0)
    sharpe = np.sqrt(12) * smartmean(ret, axis=0) / smartstd(ret, axis=0)

    print("Avg ann return=%7.4f Sharpe ratio=%7.4f" % (avgannret, sharpe))
    # Output should be
    # Avg ann return=-0.9167 Sharpe ratio=-0.1055
    # 输出应为年化平均收益率=-0.9167 夏普比率=-0.1055


if __name__ == "__main__":
    main()
