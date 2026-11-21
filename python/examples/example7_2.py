"""Port of ``example7_2.m``: cointegration test between GLD and GDX.

The book says the CADF t-statistic should be -3.35698533, the AR(1) estimate
-0.060892, the critical values -3.819 / -3.343 / -3.042 and the hedge ratio
1.6766.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.cadf import cadf
from epchan.get_tday import get_tday
from epchan.matlab_compat import intersect, union
from epchan.ols import ols
from epchan.paths import data_path
from epchan.plotting import get_pyplot
from epchan.prt import prt


def main():
    tday1, adjcls1 = get_tday(data_path("GLD.xls"))
    tday2, adjcls2 = get_tday(data_path("GDX.xls"))

    tday = union(tday1, tday2)  # find all the days when either GLD or GDX has data.

    _common, idx, idx1 = intersect(tday, tday1)
    adjcls = np.full((len(tday), 2), np.nan)  # combining the two price series
    adjcls[idx, 0] = adjcls1[idx1]

    _common, idx, idx2 = intersect(tday, tday2)
    adjcls[idx, 1] = adjcls2[idx2]

    baddata = np.flatnonzero(~np.isfinite(adjcls).all(axis=1))  # days where any one price is missing

    tday = np.delete(tday, baddata)
    adjcls = np.delete(adjcls, baddata, axis=0)

    vnames = ["GLD", "GDX"]

    # run cointegration check using augmented Dickey-Fuller test
    res = cadf(adjcls[:, 0], adjcls[:, 1], 0, 1)

    prt(res, vnames)

    # The t-statistic of -3.36 which is in between the 1% Crit Value of -3.819
    # and the 5% Crit Value of -3.343 means that there is a better than 95%
    # probability that these 2 time series are cointegrated.

    results = ols(adjcls[:, 0], adjcls[:, 1])

    hedge_ratio = float(results.beta[0, 0])
    z = results.resid

    # A hedgeRatio of 1.6766 was found. I.e. GLD=1.6766*GDX + z, where z can be
    # interpreted as the spread GLD-1.6766*GDX and should be stationary.
    print("hedgeRatio = %.4f   (the book says 1.6766)" % hedge_ratio)

    plt = get_pyplot()
    if plt is not None:
        plt.plot(z)  # This should produce a chart similar to Figure 7.4.
        plt.show()
    return res, hedge_ratio


if __name__ == "__main__":
    main()
