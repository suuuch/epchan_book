"""Port of ``example3_6.m``: pairs trading GLD against GDX.

The book says the Sharpe ratio should be about 2.3 on the training set and
about 1.5 on the test set.
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
    tday1, adjcls1 = get_tday(data_path("GLD.xls"))
    tday2, adjcls2 = get_tday(data_path("GDX.xls"))

    # find the intersection of the two data sets, and sort them in ascending order
    tday, idx1, idx2 = intersect(tday1, tday2)

    cl1 = adjcls1[idx1]
    cl2 = adjcls2[idx2]

    trainset = np.arange(0, 252)  # define indices for training set
    testset = np.arange(252, len(tday))  # define indices for test set

    # determines the hedge ratio on the trainset
    results = ols(cl1[trainset], cl2[trainset])
    hedge_ratio = float(results.beta[0, 0])

    spread = cl1 - hedge_ratio * cl2  # spread = GLD - hedgeRatio*GDX

    plt = get_pyplot()
    if plt is not None:
        plt.plot(spread[trainset])
        plt.figure()
        plt.plot(spread[testset])
        plt.figure()

    spread_mean = spread[trainset].mean()  # mean of spread on trainset
    spread_std = spread[trainset].std()  # standard deviation of spread on trainset

    zscore = (spread - spread_mean) / spread_std  # z-score of spread

    longs = zscore <= -2  # buy spread when its value drops below 2 standard deviations.
    shorts = zscore >= 2  # short spread when its value rises above 2 standard deviations.
    exits = np.abs(zscore) <= 1  # exit any spread position within 1 standard deviation.

    positions = np.full((len(tday), 2), np.nan)  # initialize positions array

    positions[shorts, :] = np.tile([-1, 1], (int(shorts.sum()), 1))  # short entries
    positions[longs, :] = np.tile([1, -1], (int(longs.sum()), 1))  # long entries
    positions[exits, :] = np.zeros((int(exits.sum()), 2))  # exit positions

    # ensure existing positions are carried forward unless there is an exit signal
    positions = fill_missing_data(positions)

    cl = np.column_stack([cl1, cl2])  # combine the 2 price series

    dailyret = (cl - lag1(cl)) / lag1(cl)

    pnl = np.sum(lag1(positions) * dailyret, axis=1)

    sharpe_trainset = (np.sqrt(252) * pnl[trainset[1:]].mean() / pnl[trainset[1:]].std())
    print("sharpeTrainset = %.4f   (the book says about 2.3)" % sharpe_trainset)

    sharpe_testset = np.sqrt(252) * pnl[testset].mean() / pnl[testset].std()
    print("sharpeTestset  = %.4f   (the book says about 1.5)" % sharpe_testset)

    if plt is not None:
        plt.plot(np.cumsum(pnl[testset]))
        plt.show()

    # save positions file for checking look-ahead bias.
    out = data_path("example3_6_positions.npz")
    np.savez(out, positions=positions)
    print("saved %s" % out)
    return sharpe_trainset, sharpe_testset


if __name__ == "__main__":
    main()
