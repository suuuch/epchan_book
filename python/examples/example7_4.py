"""Port of ``example7_4.m``: a factor model based momentum strategy.

The book says the annualised average return of the trading strategy is a very
poor -1.8099.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from scipy.io import loadmat

from epchan.backshift import backshift
from epchan.fill_missing_data import fill_missing_data
from epchan.lag1 import lag1
from epchan.ols import ols
from epchan.paths import data_path
from epchan.smartcov import smartcov
from epchan.smartmean import smartmean
from epchan.smartsum import smartsum


def main():
    lookback = 252  # use lookback days as estimation (training) period
    num_factors = 5
    topn = 50  # long stocks with topN expected 1-day returns

    # test on SP600 smallcap stocks.
    mat = loadmat(data_path("IJR_20080114.mat"))
    tday = mat["tday"].ravel()
    cl = mat["cl"]

    mycls = fill_missing_data(cl)

    positions_table = np.zeros_like(cl)

    # note the rows of dailyret are the observations at different time periods
    dailyret = (mycls - lag1(mycls)) / lag1(mycls)

    # ``i`` is the 0-based row of day ``t`` of the MATLAB loop
    # ``for t=lookback+1:length(tday)``.
    for i in range(lookback, len(tday)):
        # here the columns of R are the different observations.
        R = dailyret[i - lookback + 1:i + 1, :].T

        has_data = np.flatnonzero(np.all(np.isfinite(R), axis=1))  # avoid stocks with missing returns

        R = R[has_data, :]

        # ``avg_r`` is a column vector, as in MATLAB's ``smartmean(R, 2)``.
        avg_r = smartmean(R, axis=1).reshape(-1, 1)
        R = R - avg_r  # subtract mean from returns

        cov_r = smartcov(R.T)  # compute covariance matrix, with observations in rows.

        # X is the factor exposures matrix, B the variances of factor returns.
        # MATLAB's eig() returns the eigenvalues in ascending order; numpy's
        # eigh() does the same but returns them *before* the eigenvectors.
        _B, X = np.linalg.eigh(cov_r)

        X = X[:, X.shape[1] - num_factors:]  # Retain only numFactors

        # b are the factor returns for time period t-1 to t.
        results = ols(R[:, -1], X)
        b = results.beta

        # Rexp is the expected return for next period assuming factor returns
        # remain constant.
        rexp = (avg_r + X @ b).ravel()

        idx_sort = np.argsort(rexp, kind="stable")

        # short topN stocks with lowest expected returns
        positions_table[i, has_data[idx_sort[:topn]]] = -1
        # buy topN stocks with highest expected returns
        positions_table[i, has_data[idx_sort[-topn:]]] = 1

    # compute daily returns of trading strategy
    ret = smartsum(backshift(1, positions_table) * dailyret, axis=1)
    avgret = smartmean(ret) * 252  # compute annualized average return
    print("avgret = %.4f   (the book says -1.8099)" % avgret)
    return avgret


if __name__ == "__main__":
    main()
