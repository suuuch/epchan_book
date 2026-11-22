"""Port of ``example7_6.m``: the January effect on SP600 smallcap stocks.

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

The book says the portfolio returns should be

    Last holding date 20051230: Portfolio return=-0.0244
    Last holding date 20061229: Portfolio return=-0.0068
    Last holding date 20071231: Portfolio return= 0.0881

书中给出的投资组合收益率应为

    最后持仓日 20051230: 投资组合收益率=-0.0244
    最后持仓日 20061229: 投资组合收益率=-0.0068
    最后持仓日 20071231: 投资组合收益率= 0.0881
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

from epchan.assert_ import assert_
from epchan.fwdshift import fwdshift
from epchan.matlab_compat import matlab_round
from epchan.paths import data_path
from epchan.smartmean import smartmean


def main():
    mat = loadmat(data_path("IJR_20080131.mat"))
    tday = mat["tday"].ravel()
    cl = mat["cl"]

    # save('myfile.mat','-v6');
    # 保存为 MAT 文件 save('myfile.mat','-v6');

    onewaytcost = 0.0005  # 5bp one way transaction cost
    # 单边交易成本 5bp

    # years=year(cellstr(datestr(datenum(cellstr(num2str(tday)),
    # 'yyyymmdd'))));
    # months=month(cellstr(datestr(datenum(cellstr(num2str(tday)),
    # 'yyyymmdd'))));
    # 提取年份 years=year(cellstr(datestr(datenum(cellstr(num2str(tday)),
    # 'yyyymmdd'))));
    # 提取月份 months=month(cellstr(datestr(datenum(cellstr(num2str(tday)),
    # 'yyyymmdd'))));
    years = np.fix(tday / 10000)
    months = np.fix(np.mod(tday, 10000) / 100)

    nextdayyear = fwdshift(1, years)
    nextdaymonth = fwdshift(1, months)

    lastdayofdec = np.flatnonzero((months == 12) & (nextdaymonth == 1))
    lastdayofjan = np.flatnonzero((months == 1) & (nextdaymonth == 2))

    # lastdayofDec starts in 2004, so remove 2004 from lastdayofJan
    # lastdayofDec 从 2004 年开始，因此从 lastdayofJan 中删除 2004 年
    lastdayofjan = lastdayofjan[1:]
    # Ensure each lastdayofJan date after each lastdayofDec date
    # 确保每个 lastdayofJan 日期都晚于相应的 lastdayofDec 日期
    assert_(bool(np.all(tday[lastdayofjan] > tday[lastdayofdec])))

    eoy = np.flatnonzero(years != nextdayyear)  # End Of Year indices
    # 年末索引

    eoy = eoy[:-1]  # last index is not End of Year
    # 最后一个索引不是年末

    # Ensure eoy dates match lastdayofDec dates
    # 确保 eoy 日期与 lastdayofDec 日期一致
    assert_(bool(np.all(tday[eoy] == tday[lastdayofdec])))

    # annual returns
    # 年度收益率
    annret = (cl[eoy[1:], :] - cl[eoy[:-1], :]) / cl[eoy[:-1], :]
    # January returns
    # 一月收益率
    janret = (cl[lastdayofjan[1:], :] - cl[lastdayofdec[1:], :]) \
        / cl[lastdayofdec[1:], :]

    for y in range(annret.shape[0]):
        # pick those stocks with valid annual returns
        # 挑选年度收益率有效的股票
        has_data = np.flatnonzero(np.isfinite(annret[y, :]))
        # sort stocks based on prior year's returns
        # 按上一年度收益率对股票排序
        sortidx = np.argsort(annret[y, has_data], kind="stable")

        # buy stocks with lowest decile of returns, and vice versa for highest decile
        # 买入收益率最低十分位的股票，对最高十分位则反之
        topn = int(matlab_round(len(has_data) / 10))  # MATLAB round

        # portfolio returns
        # 投资组合收益率
        portret = (smartmean(janret[y, has_data[sortidx[:topn]]], axis=0)
                   - smartmean(janret[y, has_data[sortidx[-topn:]]], axis=0)) / 2 \
                  - 2 * onewaytcost
        print("Last holding date %d: Portfolio return=%7.4f"
              % (int(tday[lastdayofdec[y + 1]]), portret))

    # These should be the output
    # Last holding date 20051230: Portfolio return=-0.0244
    # Last holding date 20061229: Portfolio return=-0.0068
    # Last holding date 20071231: Portfolio return= 0.0881
    # 输出结果应如下
    # 最后持仓日 20051230: 投资组合收益率=-0.0244
    # 最后持仓日 20061229: 投资组合收益率=-0.0068
    # 最后持仓日 20071231: 投资组合收益率= 0.0881


if __name__ == "__main__":
    main()
