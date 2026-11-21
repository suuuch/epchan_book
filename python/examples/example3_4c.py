"""Port of ``example3_4c.m``: maximum drawdown of the market neutral strategy.

The book says the maximum drawdown should be 0.1053 and the maximum drawdown
duration 497 days.
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
    dailyret = (cls[1:] - cls[:-1]) / cls[:-1]
    excess_ret = dailyret - 0.04 / 252
    sharpe_ratio = np.sqrt(252) * excess_ret.mean() / excess_ret.std()
    print("sharpeRatio (IGE)        = %.4f   (the book says 0.7893)" % sharpe_ratio)

    cls = get_cls(data_path("SPY.xls"))
    dailyret_spy = (cls[1:] - cls[:-1]) / cls[:-1]
    net_ret = (dailyret - dailyret_spy) / 2
    sharpe_ratio = np.sqrt(252) * net_ret.mean() / net_ret.std()
    print("sharpeRatio (IGE vs SPY) = %.4f   (the book says 0.7837)" % sharpe_ratio)

    cumret = np.cumprod(1 + net_ret) - 1  # cumulative compounded returns

    plt = get_pyplot()
    if plt is not None:
        plt.plot(cumret)
        plt.show()

    max_drawdown, max_drawdown_duration = calculate_maxdd(cumret)
    print("maxDrawdown        = %.4f   (the book says 0.1053)" % max_drawdown)
    print("maxDrawdownDuration = %.0f    (the book says 497)" % max_drawdown_duration)
    return max_drawdown, max_drawdown_duration


if __name__ == "__main__":
    main()
