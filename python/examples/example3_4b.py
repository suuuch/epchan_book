"""Port of ``example3_4b.m``: the same as ``example3_4a`` but using ``getCls``.
``example3_4b.m`` 的 Python 移植：与 ``example3_4a`` 相同，但改用 ``getCls``。

The book says the Sharpe ratio should be 0.7893 for IGE alone and 0.7837 for
the market neutral portfolio.
书中给出的夏普比率：单独持有 IGE 为 0.7893，市场中性组合为 0.7837。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.get_cls import get_cls
from epchan.paths import data_path


def main():
    cls = get_cls(data_path("IGE.xls"))

    dailyret = (cls[1:] - cls[:-1]) / cls[:-1]  # daily returns
    # 每日收益率

    # excess daily returns = strategy returns - financing cost, assuming a
    # risk-free rate of 4% per annum and 252 trading days in a year
    # 超额每日收益率 = 策略收益率 - 融资成本，假设年化无风险利率为 4%，
    # 一年有 252 个交易日
    excess_ret = dailyret - 0.04 / 252
    sharpe_ratio = np.sqrt(252) * excess_ret.mean() / excess_ret.std()
    # the output should be 0.7893
    # 输出结果应为 0.7893
    print("sharpeRatio (IGE)        = %.4f   (the book says 0.7893)" % sharpe_ratio)

    cls = get_cls(data_path("SPY.xls"))  # sort cls into ascending order of dates.
    # 按日期升序排列 cls。
    dailyret_spy = (cls[1:] - cls[:-1]) / cls[:-1]  # daily returns
    # 每日收益率

    # net daily returns (divide by 2 because we now have twice as much capital.)
    # 净每日收益率（除以 2，因为现在我们有双倍的资本。）
    net_ret = (dailyret - dailyret_spy) / 2
    sharpe_ratio = np.sqrt(252) * net_ret.mean() / net_ret.std()
    # the output should be 0.7837
    # 输出结果应为 0.7837
    print("sharpeRatio (IGE vs SPY) = %.4f   (the book says 0.7837)" % sharpe_ratio)
    return sharpe_ratio


if __name__ == "__main__":
    main()
