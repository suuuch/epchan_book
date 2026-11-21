"""Port of ``example7_6.m``: the January effect on SP600 smallcap stocks.

The book says the portfolio returns should be

    Last holding date 20051230: Portfolio return=-0.0244
    Last holding date 20061229: Portfolio return=-0.0068
    Last holding date 20071231: Portfolio return= 0.0881
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from scipy.io import loadmat

from epchan.assert_ import assert_
from epchan.fwdshift import fwdshift
from epchan.matlab_compat import matlab_round
from epchan.paths import data_path
from epchan.smartmean import smartmean


def main():
    mat = loadmat(data_path("IJR_20080131.mat"))
    tday = mat["tday"].ravel()
    cl = mat["cl"]

    onewaytcost = 0.0005  # 5bp one way transaction cost

    years = np.fix(tday / 10000)
    months = np.fix(np.mod(tday, 10000) / 100)

    nextdayyear = fwdshift(1, years)
    nextdaymonth = fwdshift(1, months)

    lastdayofdec = np.flatnonzero((months == 12) & (nextdaymonth == 1))
    lastdayofjan = np.flatnonzero((months == 1) & (nextdaymonth == 2))

    # lastdayofDec starts in 2004, so remove 2004 from lastdayofJan
    lastdayofjan = lastdayofjan[1:]
    # Ensure each lastdayofJan date after each lastdayofDec date
    assert_(bool(np.all(tday[lastdayofjan] > tday[lastdayofdec])))

    eoy = np.flatnonzero(years != nextdayyear)  # End Of Year indices

    eoy = eoy[:-1]  # last index is not End of Year

    # Ensure eoy dates match lastdayofDec dates
    assert_(bool(np.all(tday[eoy] == tday[lastdayofdec])))

    # annual returns
    annret = (cl[eoy[1:], :] - cl[eoy[:-1], :]) / cl[eoy[:-1], :]
    # January returns
    janret = (cl[lastdayofjan[1:], :] - cl[lastdayofdec[1:], :]) / cl[lastdayofdec[1:], :]

    for y in range(annret.shape[0]):
        has_data = np.flatnonzero(np.isfinite(annret[y, :]))  # stocks with valid annual returns
        sortidx = np.argsort(annret[y, has_data], kind="stable")  # sort by prior year's returns

        # buy stocks with the lowest decile of returns, and vice versa for the
        # highest decile
        topn = int(matlab_round(len(has_data) / 10))  # MATLAB round

        # portfolio returns
        portret = (smartmean(janret[y, has_data[sortidx[:topn]]], axis=0)
                   - smartmean(janret[y, has_data[sortidx[-topn:]]], axis=0)) / 2 \
                  - 2 * onewaytcost
        print("Last holding date %d: Portfolio return=%7.4f"
              % (int(tday[lastdayofdec[y + 1]]), portret))


if __name__ == "__main__":
    main()
