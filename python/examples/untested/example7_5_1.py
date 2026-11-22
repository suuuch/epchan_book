"""Port of ``untested/example7_5_1.m``: example 7.5 plus the cointegration test.
``untested/example7_5_1.m`` 的 Python 移植：例 7.5 及其协整检验。

The book says the hedge ratio is 1.6766 and the half life 10.0037 days.

书中给出的对冲比率为 1.6766，半衰期为 10.0037 天。

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com

编写者:
Ernest Chan，《Quantitative Trading: How to Start Your Own Algorithmic Trading
Business》一书的作者
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np

from epchan.backshift import backshift
from epchan.cadf import cadf
from epchan.get_tday import get_tday
from epchan.matlab_compat import intersect, union
from epchan.ols import ols
from epchan.paths import data_path
from epchan.plotting import get_pyplot
from epchan.prt import prt


def main():
    """Cointegration test on GLD/GDX, the hedge ratio and the half life.
    对 GLD/GDX 做协整检验，并求出对冲比率与半衰期。
    """
    # read a spreadsheet named "GLD.xls" into MATLAB; the first column holds the
    # trading days (converted into yyyymmdd) and the last column holds the
    # adjusted close prices.
    # 将名为 "GLD.xls" 的电子表格读入 MATLAB；第一列是交易日（已转换为
    # yyyymmdd 格式），最后一列包含复权收盘价。
    tday1, adjcls1 = get_tday(data_path("GLD.xls"))
    # read a spreadsheet named "GDX.xls" into MATLAB; the first column holds the
    # trading days (converted into yyyymmdd) and the last column holds the
    # adjusted close prices.
    # 将名为 "GDX.xls" 的电子表格读入 MATLAB；第一列是交易日（已转换为
    # yyyymmdd 格式），最后一列包含复权收盘价。
    tday2, adjcls2 = get_tday(data_path("GDX.xls"))

    tday = union(tday1, tday2)  # find all the days when either GLD or GDX has data.
    # 找出 GLD 或 GDX 任一有数据的全部交易日。

    _common, idx, idx1 = intersect(tday, tday1)
    adjcls = np.full((len(tday), 2), np.nan)  # combining the two price series
    # 合并两条价格序列
    adjcls[idx, 0] = adjcls1[idx1]

    _common, idx, idx2 = intersect(tday, tday2)
    adjcls[idx, 1] = adjcls2[idx2]

    # days where a price is missing
    # 任一价格缺失的交易日
    baddata = np.flatnonzero(~np.isfinite(adjcls).all(axis=1))

    tday = np.delete(tday, baddata)
    adjcls = np.delete(adjcls, baddata, axis=0)

    vnames = ["GLD", "GDX"]

    # run cointegration check using augmented Dickey-Fuller test
    # 使用增广 Dickey-Fuller 检验进行协整检验
    res = cadf(adjcls[:, 0], adjcls[:, 1], 0, 1)

    prt(res, vnames)

    # Output from cadf function:
    # cadf 函数的输出：

    #  Augmented DF test for co-integration variables:                        GLD,GDX
    # CADF t-statistic        # of lags   AR(1) estimate
    #      -3.35698533                1        -0.060892
    #
    #    1% Crit Value    5% Crit Value   10% Crit Value
    #           -3.819           -3.343           -3.042
    # 协整变量的增广 DF 检验：                        GLD,GDX
    # CADF t 统计量        滞后阶数   AR(1) 估计值
    # 1% 临界值    5% 临界值   10% 临界值

    # The t-statistic of -3.36 which is in between the 1% Crit Value of -3.819
    # and the 5% Crit Value of -3.343 means that there is a better than 95%
    # probability that these 2 time series are cointegrated.
    # t 统计量为 -3.36，介于 1% 临界值 -3.819
    # 与 5% 临界值 -3.343 之间，说明这两个时间序列
    # 协整的概率超过 95%。

    results = ols(adjcls[:, 0], adjcls[:, 1])

    hedge_ratio = float(results.beta[0, 0])
    z = results.resid

    # A hedgeRatio of 1.6766 was found. I.e. GLD=1.6766*GDX + z, where z can be
    # interpreted as the spread GLD-1.6766*GDX and should be stationary.
    # 得到的 hedgeRatio 为 1.6766，即 GLD=1.6766*GDX + z，其中 z 可以解释为
    # 价差 GLD-1.6766*GDX，并且应当是平稳的。
    print("hedgeRatio = %.4f   (the book says 1.6766)" % hedge_ratio)

    plt = get_pyplot()
    if plt is not None:
        plt.plot(z)  # This should produce a chart similar to Figure 7.4.
        # 这应该产生与图 7.4 相似的图表。
        plt.show()

    prevz = backshift(1, z)  # z at a previous time-step
    # 上一个时间步的 z
    dz = z - prevz
    dz = dz[1:]
    prevz = prevz[1:]
    # assumes dz=theta*(z-mean(z))dt+w, where w is error term
    # 假定 dz=theta*(z-mean(z))dt+w，其中 w 为误差项
    results = ols(dz, prevz - prevz.mean())
    theta = results.beta

    halflife = -np.log(2) / theta
    # halflife =
    #
    #    10.0037
    # 半衰期 =
    print("halflife = %.4f   (the book says 10.0037)" % halflife[0, 0])
    return halflife


if __name__ == "__main__":
    main()
