"""Port of ``example3_4b.m``: the same as ``example3_4a`` but using ``getCls``.

The book says the Sharpe ratio should be 0.7893 for IGE alone and 0.7837 for
the market neutral portfolio.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.get_cls import get_cls
from epchan.paths import data_path


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
    return sharpe_ratio


if __name__ == "__main__":
    main()
