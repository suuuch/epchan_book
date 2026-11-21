"""Port of ``example7_3.m``: cointegration test between KO and PEP.

The book says the CADF t-statistic should be -2.14258438, the AR(1) estimate
-0.001167, the critical values -3.880 / -3.359 / -3.038 and the hedge ratio
1.0114.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.cadf import cadf
from epchan.get_tday import get_tday
from epchan.lag1 import lag1
from epchan.matlab_compat import intersect, union
from epchan.ols import ols
from epchan.paths import data_path
from epchan.plotting import get_pyplot
from epchan.prt import prt


def main():
    tday1, adjcls1 = get_tday(data_path("KO.xls"))
    tday2, adjcls2 = get_tday(data_path("PEP.xls"))

    tday = union(tday1, tday2)  # find all the days when either KO or PEP has data.

    _common, idx, idx1 = intersect(tday, tday1)
    adjcls = np.full((len(tday), 2), np.nan)  # combining the two price series
    adjcls[idx, 0] = adjcls1[idx1]

    _common, idx, idx2 = intersect(tday, tday2)
    adjcls[idx, 1] = adjcls2[idx2]

    baddata = np.flatnonzero(~np.isfinite(adjcls).all(axis=1))  # days where any one price is missing

    tday = np.delete(tday, baddata)
    adjcls = np.delete(adjcls, baddata, axis=0)

    vnames = ["KO", "PEP"]

    # run cointegration check using augmented Dickey-Fuller test
    res = cadf(adjcls[:, 0], adjcls[:, 1], 0, 1)

    prt(res, vnames)

    # The t-statistic of -2.14 is larger than the 10% Crit Value of -3.038
    # which means that there is a less than 90% probability that these 2 time
    # series are cointegrated.

    results = ols(adjcls[:, 0], adjcls[:, 1])

    hedge_ratio = float(results.beta[0, 0])
    z = results.resid

    # A hedgeRatio of 1.0114 was found. I.e. KO=1.0114*PEP + z, where z can be
    # interpreted as the spread KO-1.0114*PEP, which is not stationary here.
    print("hedgeRatio = %.4f   (the book says 1.0114)" % hedge_ratio)

    plt = get_pyplot()
    if plt is not None:
        plt.plot(z)  # This should produce a chart similar to Figure 7.2.
        plt.show()

    # A test for correlation.
    daily_returns = (adjcls - lag1(adjcls)) / lag1(adjcls)
    r = np.corrcoef(daily_returns[1:, :], rowvar=False)

    # The P value of 0 indicates that the two time series are significantly
    # correlated.
    print("correlation matrix =\n%s" % r)
    return res, hedge_ratio


if __name__ == "__main__":
    main()
