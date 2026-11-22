"""Port of ``untested/example3_6_1.m``: look-ahead bias check for example 3.6.
``untested/example3_6_1.m`` 的 Python 移植：例 3.6 的前视偏差检验。

The strategy should be unchanged when the last 60 trading days are removed,
which proves that it does not peek at the future.  Run ``example3_6.py``
first, it saves the ``example3_6_positions.npz`` file this script compares
against.

当删掉最近 60 个交易日之后策略结果应当保持不变，这才说明它没有偷看未来。
请先运行 ``example3_6.py``，它会保存本脚本用来比对的
``example3_6_positions.npz`` 文件。

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

from epchan.cadf import cadf
from epchan.fill_missing_data import fill_missing_data
from epchan.get_tday import get_tday
from epchan.lag1 import lag1
from epchan.matlab_compat import intersect
from epchan.ols import ols
from epchan.paths import data_path
from epchan.plotting import get_pyplot
from epchan.prt import prt


def main():
    """Recompute the GLD/GDX pairs strategy without the last 60 days.
    删掉最后 60 个交易日后重新计算 GLD/GDX 的配对交易策略。
    """
    # read a spreadsheet named "GLD.xls" into MATLAB.
    # 将名为 "GLD.xls" 的电子表格读入 MATLAB。
    tday1, adjcls1 = get_tday(data_path("GLD.xls"))
    # read a spreadsheet named "GDX.xls" into MATLAB.
    # 将名为 "GDX.xls" 的电子表格读入 MATLAB。
    tday2, adjcls2 = get_tday(data_path("GDX.xls"))

    # find the intersection of the two data sets, and sort them in ascending order
    # 求两个数据集的交集，并按升序排列
    tday, idx1, idx2 = intersect(tday1, tday2)

    cl1 = adjcls1[idx1]
    cl2 = adjcls2[idx2]

    # step one of look-forward bias check
    # 前视偏差检验第一步
    cutoff = 60  # number of most recent trading days to cut off
    # 要截断的最近交易日数量
    tday = tday[:-cutoff]  # remove the last cutoff number of days.
    # 删除最后 cutoff 天的数据。
    cl1 = cl1[:-cutoff]
    cl2 = cl2[:-cutoff]

    trainset = np.arange(0, 252)  # define indices for training set
    # 定义训练集的索引
    testset = np.arange(252, len(tday))  # define indices for test set
    # 定义测试集的索引

    vnames = ["GLD", "GDX"]

    # test for cointegration of GLD and GDX in the trainset.
    # 检验 GLD 与 GDX 在训练集中的协整性。
    res = cadf(cl1[trainset], cl2[trainset], 0, 1)

    prt(res, vnames)

    # determines the hedge ratio on the trainset
    # 在训练集上确定对冲比率
    results = ols(cl1[trainset], cl2[trainset])
    hedge_ratio = float(results.beta[0, 0])

    spread = cl1 - hedge_ratio * cl2  # spread = GLD - hedgeRatio*GDX
    # 价差 spread = GLD - hedgeRatio*GDX

    plt = get_pyplot()
    if plt is not None:
        plt.plot(spread[trainset])
        plt.figure()
        plt.plot(spread[testset])
        plt.figure()

    spread_mean = spread[trainset].mean()  # mean of spread on trainset
    # 训练集上 spread 的均值
    spread_std = spread[trainset].std()  # standard deviation of spread on trainset
    # 训练集上 spread 的标准差

    zscore = (spread - spread_mean) / spread_std  # z-score of spread
    # spread 的 z 分数

    longs = zscore <= -2  # buy spread when its value drops below 2 standard deviations.
    # 当 spread 的值跌至 2 个标准差以下时买入 spread。
    # short spread when its value rises above 2 standard deviations.
    # 当 spread 的值升至 2 个标准差以上时做空 spread。
    shorts = zscore >= 2
    exits = np.abs(zscore) <= 1  # exit any spread position within 1 standard deviation.
    # 当 spread 的值回到其均值 1 个标准差以内时平掉所有 spread 持仓。

    positions = np.full((len(tday), 2), np.nan)  # initialize positions array
    # 初始化 positions 数组

    positions[shorts, :] = np.tile([-1, 1], (int(shorts.sum()), 1))  # long entries
    # 多头入场
    positions[longs, :] = np.tile([1, -1], (int(longs.sum()), 1))  # short entries
    # 空头入场
    positions[exits, :] = np.zeros((int(exits.sum()), 2))  # exit positions
    # 平仓

    # ensure existing positions are carried forward unless there is an exit signal
    # 确保在没有平仓信号时沿用原有持仓
    positions = fill_missing_data(positions)

    cl = np.column_stack([cl1, cl2])  # combine the 2 price series
    # 合并两条价格序列

    dailyret = (cl - lag1(cl)) / lag1(cl)

    pnl = np.sum(lag1(positions) * dailyret, axis=1)

    sharpe_trainset = (np.sqrt(252) * pnl[trainset[1:]].mean()
                       / pnl[trainset[1:]].std())
    # the Sharpe ratio on the training set should be about 2.9
    # 训练集上的夏普比率应约为 2.9
    print("sharpeTrainset = %.4f   (the book says about 2.9)" % sharpe_trainset)

    sharpe_testset = np.sqrt(252) * pnl[testset].mean() / pnl[testset].std()
    # the Sharpe ratio on the test set should be about 1.0
    # 测试集上的夏普比率应约为 1.0
    print("sharpeTestset  = %.4f   (the book says about 1.0)" % sharpe_testset)

    if plt is not None:
        plt.plot(np.cumsum(pnl[testset]))
        plt.show()

    # step two of look-forward-bias check
    # 前视偏差检验第二步
    oldoutput = np.load(data_path("example3_6_positions.npz"))["positions"]
    oldoutput = oldoutput[:-cutoff, :]

    if np.any(positions != oldoutput):
        print("Program has look-forward-bias!")
    else:
        print("No look-forward-bias: the positions are unchanged.")
    return positions, oldoutput


if __name__ == "__main__":
    main()
