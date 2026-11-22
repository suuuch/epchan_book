"""Port of ``example6_3.m``: Kelly optimal leverages for oil futures.

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

The book says the annualised mean excess returns are
``[0.1396, 0.0294, -0.0073]``, the maximum annualised compounded growth
rate is 0.1529 and the Sharpe ratio of the portfolio is 0.4751.
书中给出的年化平均超额收益率为 ``[0.1396, 0.0294, -0.0073]``，
最大年化复合增长率为 0.1529，投资组合的夏普比率为 0.4751。
"""

import sys
from pathlib import Path

# Add this folder to the Python path, just like the MATLAB original adds this
# folder and the data folder to the MATLAB path.
# 将本文件夹添加到 Python 路径中，就像 MATLAB 原版把本文件夹和数据文件夹
# 添加到 MATLAB 路径中那样。
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.get_tday import get_tday
from epchan.lag1 import lag1
from epchan.matlab_compat import intersect, union
from epchan.paths import data_path


def main():
    # [num1, txt1]=xlsread('OIH'); % read a spreadsheet named "OIH.xls" into
    # MATLAB.
    # 将名为 "OIH.xls" 的电子表格读入 MATLAB。
    #
    # tday1=txt1(2:end, 1); % the first column (starting from the second row) is
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
    # adjcls1=num1(:, end); % the last column contains the adjusted close
    # prices.
    # 最后一列包含复权后收盘价。
    tday1, adjcls1 = get_tday(data_path("OIH.xls"))

    # [num2, txt2]=xlsread('RKH'); % read a spreadsheet named "RKH.xls" into
    # MATLAB.
    # 将名为 "RKH.xls" 的电子表格读入 MATLAB。
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
    tday2, adjcls2 = get_tday(data_path("RKH.xls"))

    # [num3, txt3]=xlsread('RTH'); % read a spreadsheet named "RTH.xls" into
    # MATLAB.
    # 将名为 "RTH.xls" 的电子表格读入 MATLAB。
    #
    # tday3=txt3(2:end, 1); % the first column (starting from the second row) is
    # the trading days in format mm/dd/yyyy.
    # 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。
    #
    # tday3=datestr(datenum(tday3, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the
    # format into yyyymmdd.
    # 将格式转换为 yyyymmdd。
    #
    # tday3=str2double(cellstr(tday3)); % convert the date strings first into
    # cell arrays and then into numeric format.
    # 先将日期字符串转换为单元格数组，然后再转换为数值格式。
    #
    # adjcls3=num3(:, end);
    # 复权后收盘价: adjcls3=num3(:, end);
    tday3, adjcls3 = get_tday(data_path("RTH.xls"))

    # merge these data
    # 合并这些数据
    tday = union(tday1, tday2)
    tday = union(tday, tday3)

    # adjcls=NaN(length(tday), 3);
    # 复权后收盘价矩阵: adjcls=NaN(length(tday), 3);
    adjcls = np.full((len(tday), 3), np.nan)

    _common, idx1, idx = intersect(tday1, tday)
    adjcls[idx, 0] = adjcls1[idx1]
    _common, idx2, idx = intersect(tday2, tday)
    adjcls[idx, 1] = adjcls2[idx2]
    _common, idx3, idx = intersect(tday3, tday)
    adjcls[idx, 2] = adjcls3[idx3]

    ret = (adjcls - lag1(adjcls)) / lag1(adjcls)  # returns
    # 收益率

    # days where any one return is missing
    # 任一收益率缺失的交易日
    baddata = np.flatnonzero(~np.isfinite(ret).all(axis=1))

    # eliminate days where any one return is missing
    # 剔除任一收益率缺失的交易日
    ret = np.delete(ret, baddata, axis=0)

    # excess returns: assume annualized risk free rate is 4%
    # 超额收益率：假设年化无风险利率为 4%
    excess_ret = ret - np.tile(0.04 / 252, ret.shape)

    m = 252 * excess_ret.mean(axis=0)  # annualized mean excess returns
    # 年化平均超额收益率
    print("M =\n%s" % m)
    # M =
    #
    #     0.1396
    #     0.0294
    #    -0.0073

    c = 252 * np.cov(excess_ret, rowvar=False)  # annualized covariance matrix
    # 年化协方差矩阵
    print("C =\n%s" % c)
    # C =
    #
    #     0.1109    0.0200    0.0183
    #     0.0200    0.0372    0.0269
    #     0.0183    0.0269    0.0420

    f = np.linalg.inv(c) @ m  # Kelly optimal leverages
    # Kelly 最优杠杆
    print("F =\n%s" % f)
    # F =
    #
    #     1.2919
    #     1.1723
    #    -1.4882

    g = 0.04 + f @ c @ f / 2  # Maximum annualized compounded growth rate
    # 最大年化复合增长率
    print("g =\n%s" % g)
    # g =
    #
    #     0.1529

    s = np.sqrt(f @ c @ f)  # Sharpe ratio of portfolio
    # 投资组合的夏普比率
    print("S =\n%s" % s)
    # S =
    #
    #     0.4751
    return m, c, f, g, s


if __name__ == "__main__":
    main()
