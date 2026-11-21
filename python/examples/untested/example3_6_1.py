"""Port of ``untested/example3_6_1.m``: look-ahead bias check for example 3.6.

The strategy should be unchanged when the last 60 trading days are removed,
which proves that it does not peek at the future.  Run ``example3_6.py``
first, it saves the ``example3_6_positions.npz`` file this script compares
against.
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
    tday1, adjcls1 = get_tday(data_path("GLD.xls"))
    tday2, adjcls2 = get_tday(data_path("GDX.xls"))

    # find the intersection of the two data sets, and sort them in ascending order
    tday, idx1, idx2 = intersect(tday1, tday2)

    cl1 = adjcls1[idx1]
    cl2 = adjcls2[idx2]

    # step one of look-forward bias check
    cutoff = 60  # number of most recent trading days to cut off
    tday = tday[:-cutoff]  # remove the last cutoff number of days.
    cl1 = cl1[:-cutoff]
    cl2 = cl2[:-cutoff]

    trainset = np.arange(0, 252)  # define indices for training set
    testset = np.arange(252, len(tday))  # define indices for test set

    vnames = ["GLD", "GDX"]

    # test for cointegration of GLD and GDX in the trainset.
    res = cadf(cl1[trainset], cl2[trainset], 0, 1)

    prt(res, vnames)

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

    positions[shorts, :] = np.tile([-1, 1], (int(shorts.sum()), 1))  # long entries
    positions[longs, :] = np.tile([1, -1], (int(longs.sum()), 1))  # short entries
    positions[exits, :] = np.zeros((int(exits.sum()), 2))  # exit positions

    # ensure existing positions are carried forward unless there is an exit signal
    positions = fill_missing_data(positions)

    cl = np.column_stack([cl1, cl2])  # combine the 2 price series

    dailyret = (cl - lag1(cl)) / lag1(cl)

    pnl = np.sum(lag1(positions) * dailyret, axis=1)

    sharpe_trainset = (np.sqrt(252) * pnl[trainset[1:]].mean() / pnl[trainset[1:]].std())
    print("sharpeTrainset = %.4f   (the book says about 2.9)" % sharpe_trainset)

    sharpe_testset = np.sqrt(252) * pnl[testset].mean() / pnl[testset].std()
    print("sharpeTestset  = %.4f   (the book says about 1.0)" % sharpe_testset)

    if plt is not None:
        plt.plot(np.cumsum(pnl[testset]))
        plt.show()

    # step two of look-forward-bias check
    oldoutput = np.load(data_path("example3_6_positions.npz"))["positions"]
    oldoutput = oldoutput[:-cutoff, :]

    if np.any(positions != oldoutput):
        print("Program has look-forward-bias!")
    else:
        print("No look-forward-bias: the positions are unchanged.")
    return positions, oldoutput


if __name__ == "__main__":
    main()
