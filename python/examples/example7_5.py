"""Port of ``example7_5.m``: the half life of the GLD/GDX spread.

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

The book says the hedge ratio is 1.6766 and the half life of the spread is
10.0037 days.
书中给出的对冲比率为 1.6766，价差的半衰期为 10.0037 天。
"""

import sys
from pathlib import Path

# Add this folder to the Python path, just like the MATLAB original adds this
# folder and the data folder to the MATLAB path.
# 将本文件夹添加到 Python 路径中，就像 MATLAB 原版把本文件夹和数据文件夹
# 添加到 MATLAB 路径中那样。
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.backshift import backshift
from epchan.get_tday import get_tday
from epchan.matlab_compat import intersect, union
from epchan.ols import ols
from epchan.paths import data_path


def main():
    # [num, txt]=xlsread('GLD'); % read a spreadsheet named "GLD.xls" into
    # MATLAB.
    # 将名为 "GLD.xls" 的电子表格读入 MATLAB。
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
    # 先把日期字符串转换为单元格数组，再转换为数值格式。
    #
    # adjcls1=num(:, end); % the last column contains the adjusted close prices.
    # 最后一列包含调整后的收盘价。
    tday1, adjcls1 = get_tday(data_path("GLD.xls"))

    # [num2, txt2]=xlsread('GDX'); % read a spreadsheet named "GDX.xls" into
    # MATLAB.
    # 将名为 "GDX.xls" 的电子表格读入 MATLAB。
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
    # 先把日期字符串转换为单元格数组，再转换为数值格式。
    #
    # adjcls2=num2(:, end);
    # GDX 的调整后收盘价 adjcls2=num2(:, end);
    tday2, adjcls2 = get_tday(data_path("GDX.xls"))

    tday = union(tday1, tday2)  # find all the days when either GLD or GDX has data.
    # 找出 GLD 或 GDX 任一有数据的全部交易日。

    _common, idx, idx1 = intersect(tday, tday1)

    # adjcls=NaN(length(tday), 2);
    adjcls = np.full((len(tday), 2), np.nan)  # combining the two price series
    # 合并两条价格序列
    adjcls[idx, 0] = adjcls1[idx1]

    _common, idx, idx2 = intersect(tday, tday2)

    adjcls[idx, 1] = adjcls2[idx2]

    # days where any one price is missing
    # 任一价格缺失的交易日
    baddata = np.flatnonzero(~np.isfinite(adjcls).all(axis=1))

    tday = np.delete(tday, baddata)

    adjcls = np.delete(adjcls, baddata, axis=0)

    results = ols(adjcls[:, 0], adjcls[:, 1])

    hedge_ratio = float(results.beta[0, 0])
    z = results.resid  # residuals: deviation from the mean value of the spread
    # 残差: 相对于价差均值的偏离

    # A hedgeRatio of 1.6766 was found. I.e. GLD=1.6766*GDX + z, where z can be
    # interpreted as the spread GLD-1.6766*GDX and should be stationary.
    # 得到的 hedgeRatio 为 1.6766，即 GLD=1.6766*GDX + z，其中 z 可以解释为
    # 价差 GLD-1.6766*GDX，并且应当是平稳的。
    print("hedgeRatio = %.4f   (the book says 1.6766)" % hedge_ratio)

    # ====== same as example7_1.m up to here ======
    # ====== 到此为止与 example7_1.m 相同 ======

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
