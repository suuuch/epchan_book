"""Port of ``example3_6.m``: pairs trading GLD against GDX.
``example3_6.m`` 的 Python 移植：GLD 对 GDX 的配对交易。

The book says the Sharpe ratio should be about 2.3 on the training set and
about 1.5 on the test set.
书中给出的夏普比率：训练集约为 2.3，测试集约为 1.5。

written by: Ernest Chan
编写者：Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"
著有《Quantitative Trading: How to Start Your Own Algorithmic Trading Business》
一书。

ernest@epchan.com
www.epchan.com
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.fill_missing_data import fill_missing_data
from epchan.get_tday import get_tday
from epchan.lag1 import lag1
from epchan.matlab_compat import intersect
from epchan.ols import ols
from epchan.paths import data_path
from epchan.plotting import get_pyplot


def main():
    # [num, txt]=xlsread('GLD'); % read a spreadsheet named "GLD.xls" into MATLAB.
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
    tday1, adjcls1 = get_tday(data_path("GLD.xls"))

    # adjcls1=num(:, end); % the last column contains the adjusted close prices.
    # 最后一列包含调整后的收盘价。

    # [num, txt]=xlsread('GDX'); % read a spreadsheet named "GDX.xls" into MATLAB.
    # 将名为 "GDX.xls" 的电子表格读入 MATLAB。
    #
    # tday2=txt(2:end, 1); % the first column (starting from the second row) is
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
    tday2, adjcls2 = get_tday(data_path("GDX.xls"))

    # adjcls2=num(:, end); % the last column contains the adjusted close prices.
    # 最后一列包含调整后的收盘价。

    # find the intersection of the two data sets, and sort them in ascending order
    # 求两个数据集的交集，并按升序排序
    tday, idx1, idx2 = intersect(tday1, tday2)

    cl1 = adjcls1[idx1]
    cl2 = adjcls2[idx2]

    trainset = np.arange(0, 252)  # define indices for training set
    # 定义训练集的索引
    testset = np.arange(252, len(tday))  # define indices for test set
    # 定义测试集的索引

    # determines the hedge ratio on the trainset
    # 在训练集上确定对冲比率
    results = ols(cl1[trainset], cl2[trainset])  # use regression function
    # 使用回归函数
    hedge_ratio = float(results.beta[0, 0])

    spread = cl1 - hedge_ratio * cl2  # spread = GLD - hedgeRatio*GDX
    # 即 spread = GLD - hedgeRatio*GDX

    plt = get_pyplot()
    if plt is not None:
        plt.plot(spread[trainset])
        plt.figure()
        plt.plot(spread[testset])
        plt.figure()

    spread_mean = spread[trainset].mean()  # mean of spread on trainset
    # 训练集上价差的均值
    spread_std = spread[trainset].std()  # standard deviation of spread on trainset
    # 训练集上价差的标准差

    zscore = (spread - spread_mean) / spread_std  # z-score of spread
    # 价差的 z-score

    longs = zscore <= -2  # buy spread when its value drops below 2 standard deviations.
    # 当价差跌破 2 倍标准差时买入价差。
    # short spread when its value rises above 2 standard deviations.
    # 当价差升破 2 倍标准差时做空价差。
    shorts = zscore >= 2
    # exit any spread position within 1 standard deviation.
    # 当价差处于其均值 1 倍标准差范围内时，平掉所有价差持仓。
    exits = np.abs(zscore) <= 1

    # positions=np.full((len(tday), 2), np.nan)  # initialize positions array
    # positions=np.full(len(tday), np.nan)  # initialize positions array
    # 初始化持仓数组
    # 初始化持仓数组
    positions = np.full((len(tday), 2), np.nan)

    positions[shorts, :] = np.tile([-1, 1], (int(shorts.sum()), 1))  # short entries
    # 空头入场
    positions[longs, :] = np.tile([1, -1], (int(longs.sum()), 1))  # long entries
    # 多头入场
    positions[exits, :] = np.zeros((int(exits.sum()), 2))  # exit positions
    # 平仓

    # ensure existing positions are carried forward unless there is an exit signal
    # 确保在没有平仓信号时原有持仓被延续下来
    positions = fill_missing_data(positions)

    cl = np.column_stack([cl1, cl2])  # combine the 2 price series
    # 合并两条价格序列

    dailyret = (cl - lag1(cl)) / lag1(cl)

    pnl = np.sum(lag1(positions) * dailyret, axis=1)

    sharpe_trainset = (np.sqrt(252) * pnl[trainset[1:]].mean()
                       / pnl[trainset[1:]].std())
    # the Sharpe ratio on the training set should be about 2.3
    # 训练集上的夏普比率应约为 2.3
    print("sharpeTrainset = %.4f   (the book says about 2.3)" % sharpe_trainset)

    sharpe_testset = np.sqrt(252) * pnl[testset].mean() / pnl[testset].std()
    # the Sharpe ratio on the test set should be about 1.5
    # 测试集上的夏普比率应约为 1.5
    print("sharpeTestset  = %.4f   (the book says about 1.5)" % sharpe_testset)

    if plt is not None:
        plt.plot(np.cumsum(pnl[testset]))
        plt.show()

    # save positions file for checking look-ahead bias.
    # 保存持仓文件以检查前视偏差。
    out = data_path("example3_6_positions.npz")
    np.savez(out, positions=positions)
    print("saved %s" % out)
    return sharpe_trainset, sharpe_testset


if __name__ == "__main__":
    main()
