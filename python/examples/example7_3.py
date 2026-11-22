"""Port of ``example7_3.m``: cointegration test between KO and PEP.

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com
编写者：
作者：Ernest Chan
著有《Quantitative Trading:
How to Start Your Own Algorithmic Trading Business》一书。

The book says the CADF t-statistic should be -2.14258438, the AR(1) estimate
-0.001167, the critical values -3.880 / -3.359 / -3.038 and the hedge ratio
1.0114.
书中给出的 CADF t 统计量为 -2.14258438，AR(1) 估计值为 -0.001167，
临界值为 -3.880 / -3.359 / -3.038，对冲比率为 1.0114。
"""

import sys
from pathlib import Path

# Add this folder to the Python path, just like the MATLAB original adds this
# folder and the data folder to the MATLAB path.
# 将本文件夹添加到 Python 路径中，就像 MATLAB 原版把本文件夹和数据文件夹
# 添加到 MATLAB 路径中那样。
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.cadf import cadf
from epchan.get_tday import get_tday
from epchan.lag1 import lag1
from epchan.matlab_compat import intersect, union
from epchan.ols import ols
from epchan.paths import data_path
from epchan.plotting import get_pyplot
from epchan.prt import prt


def main():
    # [num, txt]=xlsread('KO'); % read a spreadsheet named "KO.xls" into MATLAB.
    # 将名为 "KO.xls" 的电子表格读入 MATLAB。
    #
    # tday1=txt(2:end, 1); % the first column (starting from the second row) is
    # the trading days in format mm/dd/yyyy.
    # 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。
    #
    # tday1=datestr(datenum(tday1, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the
    # format into yyyymmdd.
    # 将格式转换为 yyyymmdd。
    #
    # tday1=str2double(cellstr(tday1)); % convert the date strings first into
    # cell arrays and then into numeric format.
    # 先将日期字符串转换为单元格数组，然后再转换为数值格式。
    #
    # adjcls1=num(:, end); % the last column contains the adjusted close prices.
    # 最后一列包含复权后收盘价。
    tday1, adjcls1 = get_tday(data_path("KO.xls"))

    # [num2, txt2]=xlsread('PEP'); % read a spreadsheet named "PEP.xls" into
    # MATLAB.
    # 将名为 "PEP.xls" 的电子表格读入 MATLAB。
    #
    # tday2=txt2(2:end, 1); % the first column (starting from the second row) is
    # the trading days in format mm/dd/yyyy.
    # 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。
    #
    # tday2=datestr(datenum(tday2, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the
    # format into yyyymmdd.
    # 将格式转换为 yyyymmdd。
    #
    # tday2=str2double(cellstr(tday2)); % convert the date strings first into
    # cell arrays and then into numeric format.
    # 先将日期字符串转换为单元格数组，然后再转换为数值格式。
    #
    # adjcls2=num2(:, end);
    # 复权后收盘价: adjcls2=num2(:, end);
    tday2, adjcls2 = get_tday(data_path("PEP.xls"))

    tday = union(tday1, tday2)  # find all the days when either KO or PEP has data.
    # 找出 KO 或 PEP 有数据的所有交易日。

    _common, idx, idx1 = intersect(tday, tday1)

    # adjcls=NaN(length(tday), 2);
    adjcls = np.full((len(tday), 2), np.nan)  # combining the two price series
    # 合并两个价格序列
    adjcls[idx, 0] = adjcls1[idx1]

    _common, idx, idx2 = intersect(tday, tday2)

    adjcls[idx, 1] = adjcls2[idx2]

    # days where any one price is missing
    # 任一价格缺失的交易日
    baddata = np.flatnonzero(~np.isfinite(adjcls).all(axis=1))

    tday = np.delete(tday, baddata)

    adjcls = np.delete(adjcls, baddata, axis=0)

    vnames = ["KO", "PEP"]

    # run cointegration check using augmented Dickey-Fuller test
    # 用增广 Dickey-Fuller 检验做协整检验
    res = cadf(adjcls[:, 0], adjcls[:, 1], 0, 1)

    prt(res, vnames)

    # Output from cadf function:
    # cadf 函数的输出:
    #
    #  Augmented DF test for co-integration variables:                        KO ,PEP
    # CADF t-statistic        # of lags   AR(1) estimate
    #      -2.14258438                1        -0.001167
    #
    #    1% Crit Value    5% Crit Value   10% Crit Value
    #           -3.880           -3.359           -3.038
    # 协整变量的增广 DF 检验:              KO ,PEP
    # CADF t 统计量        滞后阶数   AR(1) 估计值
    # 1% 临界值    5% 临界值   10% 临界值

    # The t-statistic of -2.14 is larger than the 10% Crit Value of -3.038
    # which means that there is a less than 90% probability that these 2 time
    # series are cointegrated.
    # -2.14 的 t 统计量大于 10% 临界值 -3.038
    # 这意味着这两个时间序列协整的概率小于 90%。

    results = ols(adjcls[:, 0], adjcls[:, 1])

    hedge_ratio = float(results.beta[0, 0])
    z = results.resid

    # A hedgeRatio of 1.0114 was found. I.e. KO=1.0114*PEP + z, where z can be
    # interpreted as the spread KO-1.0114*PEP, which is not stationary here.
    # 得到的 hedgeRatio 为 1.0114，即 KO=1.0114*PEP + z，其中 z 可以解释为
    # 价差 KO-1.0114*PEP，此处它并非平稳。
    print("hedgeRatio = %.4f   (the book says 1.0114)" % hedge_ratio)

    plt = get_pyplot()
    if plt is not None:
        plt.plot(z)  # This should produce a chart similar to Figure 7.2.
        # 这应该会生成与 Figure 7.2 相似的图形（标题和标签除外）。
        plt.show()

    # A test for correlation.
    # 相关性检验。
    daily_returns = (adjcls - lag1(adjcls)) / lag1(adjcls)
    r = np.corrcoef(daily_returns[1:, :], rowvar=False)

    # R =
    #
    #     1.0000    0.4849
    #     0.4849    1.0000
    #
    #
    # P =
    #
    #      1     0
    #      0     1

    # The P value of 0 indicates that the two time series are significantly
    # correlated.
    # P 值为 0 表明这两个时间序列显著相关。
    print("correlation matrix =\n%s" % r)
    return res, hedge_ratio


if __name__ == "__main__":
    main()
