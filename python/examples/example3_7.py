"""Port of ``example3_7.m``: market neutral strategy on the SP500 stocks.

The book says the Sharpe ratio should be about 0.25 and, once 5 basis points
of transaction costs are deducted, about -3.19.
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

    mat = loadmat(data_path("SPX_20071123.mat"))
    tday = mat["tday"].ravel()
    cl = mat["cl"]

    dailyret = (cl - lag1(cl)) / lag1(cl)  # daily returns

    market_dailyret = smartmean(dailyret, axis=1)  # equal weighted market index return

    # weight of a stock is proportional to the negative distance to the market index.
    weights = (-(dailyret - np.tile(market_dailyret.reshape(-1, 1), (1, cl.shape[1])))
               / np.tile(smartsum(np.isfinite(cl), axis=1).reshape(-1, 1), (1, cl.shape[1])))

    # those stocks that do not have valid prices or daily returns are excluded.
    weights[~np.isfinite(cl) | ~np.isfinite(lag1(cl))] = 0

    dailypnl = smartsum(lag1(weights) * dailyret, axis=1)

    outside = (tday < start_date) | (tday > end_date)
    dailypnl = dailypnl[~outside]  # remove pnl outside of our dates of interest

    sharpe = np.sqrt(252) * smartmean(dailypnl, axis=0) / smartstd(dailypnl, axis=0)
    print("sharpe = %.4f   (the book says about 0.25)" % sharpe)

    # daily pnl with transaction costs deducted
    onewaytcost = 0.0005  # assume 5 basis points

    weights = weights[~outside, :]  # remove weights outside of our dates of interest

    # transaction costs are only incurred when the weights change
    dailypnl_minustcost = dailypnl - smartsum(np.abs(weights - lag1(weights)), axis=1) * onewaytcost

    sharpe_minustcost = (np.sqrt(252) * smartmean(dailypnl_minustcost, axis=0)
                         / smartstd(dailypnl_minustcost, axis=0))
    print("sharpe (with transaction costs) = %.4f   (the book says about -3.19)"
          % sharpe_minustcost)
    return sharpe, sharpe_minustcost


if __name__ == "__main__":
    main()
