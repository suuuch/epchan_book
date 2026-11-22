"""Port of ``example3_7.m``: market neutral strategy on the SP500 stocks.
``example3_7.m`` 的 Python 移植：针对标普 500 股票的市场中性策略。

The book says the Sharpe ratio should be about 0.25 and, once 5 basis points
of transaction costs are deducted, about -3.19.
书中给出的夏普比率约为 0.25，扣除 5 个基点的交易成本后约为 -3.19。

written by: Ernest Chan
编写者：Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"
作者: 《Quantitative Trading: How to Start Your Own Algorithmic Trading Business》

ernest@epchan.com
www.epchan.com
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from scipy.io import loadmat

from epchan.lag1 import lag1
from epchan.paths import data_path
from epchan.smartmean import smartmean
from epchan.smartstd import smartstd
from epchan.smartsum import smartsum


def main():
    start_date = 20060101
    end_date = 20061231

    # load('SPX_20071123', 'tday', 'stocks', 'cl');
    # save('myfile.mat','-v6'); % save the data
    # 保存数据: save('myfile.mat','-v6');
    mat = loadmat(data_path("SPX_20071123.mat"))
    tday = mat["tday"].ravel()
    cl = mat["cl"]

    dailyret = (cl - lag1(cl)) / lag1(cl)  # daily returns
    # 每日收益率

    market_dailyret = smartmean(dailyret, axis=1)  # equal weighted market index return
    # 等权重市场指数收益率
    # In MATLAB smartmean(dailyret, 2) averages over the columns; numpy's axis
    # is 0-based, so the same call is smartmean(dailyret, axis=1).
    # MATLAB 中 smartmean(dailyret, 2) 是沿列方向求均值；numpy 的 axis 从 0
    # 开始计数，因此对应 smartmean(dailyret, axis=1)。

    # weight of a stock is proportional to the negative distance to the market index.
    # 个股权重与到市场指数的负距离成正比。
    weights = (-(dailyret - np.tile(market_dailyret.reshape(-1, 1), (1, cl.shape[1])))
               / np.tile(smartsum(np.isfinite(cl), axis=1).reshape(-1, 1),
                         (1, cl.shape[1])))

    # those stocks that do not have valid prices or daily returns are excluded.
    # 价格或每日收益率无效的股票将被剔除。
    weights[~np.isfinite(cl) | ~np.isfinite(lag1(cl))] = 0

    dailypnl = smartsum(lag1(weights) * dailyret, axis=1)

    outside = (tday < start_date) | (tday > end_date)
    dailypnl = dailypnl[~outside]  # remove pnl outside of our dates of interest
    # 剔除所关注日期范围之外的盈亏

    sharpe = np.sqrt(252) * smartmean(dailypnl, axis=0) / smartstd(dailypnl, axis=0)
    # Sharpe ratio should be about 0.25
    # 夏普比率应约为 0.25
    print("sharpe = %.4f   (the book says about 0.25)" % sharpe)

    # daily pnl with transaction costs deducted
    # 扣除交易成本后的每日盈亏
    onewaytcost = 0.0005  # assume 5 basis points
    # 假设为 5 个基点

    weights = weights[~outside, :]  # remove weights outside of our dates of interest
    # 剔除所关注日期范围之外的权重

    # transaction costs are only incurred when the weights change
    # 只有在权重发生变化时才会产生交易成本
    dailypnl_minustcost = dailypnl - smartsum(
        np.abs(weights - lag1(weights)), axis=1) * onewaytcost

    sharpe_minustcost = (np.sqrt(252) * smartmean(dailypnl_minustcost, axis=0)
                         / smartstd(dailypnl_minustcost, axis=0))
    # Sharpe ratio should be about -3.19
    # 夏普比率应约为 -3.19
    print("sharpe (with transaction costs) = %.4f   (the book says about -3.19)"
          % sharpe_minustcost)
    return sharpe, sharpe_minustcost


if __name__ == "__main__":
    main()
