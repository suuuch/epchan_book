"""Port of ``example3_4c.m``: maximum drawdown of the market neutral strategy.
``example3_4c.m`` 的 Python 移植：市场中性策略的最大回撤。

The book says the maximum drawdown should be 0.1053 and the maximum drawdown
duration 497 days.
书中给出的最大回撤为 0.1053，最大回撤持续时间为 497 天。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.calculate_maxdd import calculate_maxdd
from epchan.get_cls import get_cls
from epchan.paths import data_path
from epchan.plotting import get_pyplot


def main():
    cls = get_cls(data_path("IGE.xls"))

    dailyret = (cls[1:] - cls[:-1]) / cls[:-1]  # daily returns
    # 日收益率

    # excess daily returns = strategy returns - financing cost, assuming a
    # risk-free rate of 4% per annum and 252 trading days in a year
    # 超额日收益率 = 策略收益率 - 融资成本，假设年无风险利率为 4%，
    # 且每年有 252 个交易日
    excess_ret = dailyret - 0.04 / 252
    sharpe_ratio = np.sqrt(252) * excess_ret.mean() / excess_ret.std()
    # the output should be 0.7893
    # 输出应为 0.7893
    print("sharpeRatio (IGE)        = %.4f   (the book says 0.7893)" % sharpe_ratio)

    cls = get_cls(data_path("SPY.xls"))  # sort cls into ascending order of dates.
    # 将 cls 按日期升序排序。
    dailyret_spy = (cls[1:] - cls[:-1]) / cls[:-1]  # daily returns
    # 日收益率

    # net daily returns (divide by 2 because we now have twice as much capital.)
    # 净日收益率 (除以 2 是因为我们现在有双倍的资本)
    net_ret = (dailyret - dailyret_spy) / 2
    sharpe_ratio = np.sqrt(252) * net_ret.mean() / net_ret.std()
    # the output should be 0.7837
    # 输出应为 0.7837
    print("sharpeRatio (IGE vs SPY) = %.4f   (the book says 0.7837)" % sharpe_ratio)

    cumret = np.cumprod(1 + net_ret) - 1  # cumulative compounded returns
    # 累计复合收益率

    plt = get_pyplot()
    if plt is not None:
        plt.plot(cumret)
        plt.show()

    max_drawdown, max_drawdown_duration = calculate_maxdd(cumret)
    # maximum drawdown. Output should be 0.1053
    # 最大回撤。输出应为 0.1053
    print("maxDrawdown        = %.4f   (the book says 0.1053)" % max_drawdown)
    # maximum drawdown duration. Output should be 497.
    # 最大回撤持续时间。输出应为 497。
    print("maxDrawdownDuration = %.0f    (the book says 497)" % max_drawdown_duration)
    return max_drawdown, max_drawdown_duration


if __name__ == "__main__":
    main()
