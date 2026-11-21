"""Port of ``example6_3.m``: Kelly optimal leverages for oil futures.

The book says the annualised mean excess returns are
``[0.1396, 0.0294, -0.0073]``, the maximum annualised compounded growth
rate is 0.1529 and the Sharpe ratio of the portfolio is 0.4751.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.get_tday import get_tday
from epchan.lag1 import lag1
from epchan.matlab_compat import intersect, union
from epchan.paths import data_path


def main():
    tday1, adjcls1 = get_tday(data_path("OIH.xls"))
    tday2, adjcls2 = get_tday(data_path("RKH.xls"))
    tday3, adjcls3 = get_tday(data_path("RTH.xls"))

    # merge these data
    tday = union(tday1, tday2)
    tday = union(tday, tday3)

    adjcls = np.full((len(tday), 3), np.nan)

    _common, idx1, idx = intersect(tday1, tday)
    adjcls[idx, 0] = adjcls1[idx1]
    _common, idx2, idx = intersect(tday2, tday)
    adjcls[idx, 1] = adjcls2[idx2]
    _common, idx3, idx = intersect(tday3, tday)
    adjcls[idx, 2] = adjcls3[idx3]

    ret = (adjcls - lag1(adjcls)) / lag1(adjcls)  # returns

    # days where any one return is missing
    baddata = np.flatnonzero(~np.isfinite(ret).all(axis=1))

    ret = np.delete(ret, baddata, axis=0)  # eliminate days where any one return is missing

    # excess returns: assume annualized risk free rate is 4%
    excess_ret = ret - np.tile(0.04 / 252, ret.shape)

    m = 252 * excess_ret.mean(axis=0)  # annualized mean excess returns
    print("M =\n%s" % m)

    c = 252 * np.cov(excess_ret, rowvar=False)  # annualized covariance matrix
    print("C =\n%s" % c)

    f = np.linalg.inv(c) @ m  # Kelly optimal leverages
    print("F =\n%s" % f)

    g = 0.04 + f @ c @ f / 2  # Maximum annualized compounded growth rate
    print("g =\n%s" % g)

    s = np.sqrt(f @ c @ f)  # Sharpe ratio of portfolio
    print("S =\n%s" % s)
    return m, c, f, g, s


if __name__ == "__main__":
    main()
