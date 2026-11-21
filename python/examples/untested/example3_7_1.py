"""Port of ``untested/example3_7_1.m``: build a price matrix from an export.

The MATLAB original reads a *long* format export whose columns are

    symbol, date, open, high, low, close, volume

(``textread(inputFile, '%s %u %f %f %f %f %u', 'delimiter', ',')``) and pivots
it into the ``tday``/``stocks``/``op``/``hi``/``lo``/``cl``/``vol`` matrices
that ``example3_7`` loads.

.. note::

   The ``Export.txt`` that ships with the repository is in *wide* format
   (``Date`` followed by one column per symbol), exactly like
   ``SPX_20071123.txt``.  When a wide file is detected only the price columns
   can be recovered, so ``op``, ``hi``, ``lo`` and ``vol`` are filled with
   ``NaN``.  The output is written next to the original ``.mat`` file under
   the name ``SPX_20071123_py.mat`` so the book's data file is never
   overwritten.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from scipy.io import savemat

from epchan.matlab_compat import intersect
from epchan.paths import data_path

INPUT_FILE = data_path("Export.txt")
OUTPUT_FILE = data_path("SPX_20071123_py.mat")


def _read_long(path):
    """Read the long format the MATLAB original expects."""
    mysym, mytday, myop, myhi, mylo, mycl, myvol = [], [], [], [], [], [], []
    with open(path, encoding="latin-1") as handle:
        for line in handle:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) != 7 or not parts[1].isdigit():
                continue
            mysym.append(parts[0])
            mytday.append(int(parts[1]))
            myop.append(float(parts[2]))
            myhi.append(float(parts[3]))
            mylo.append(float(parts[4]))
            mycl.append(float(parts[5]))
            myvol.append(float(parts[6]))
    return (np.array(mysym), np.array(mytday, dtype=np.int64),
            *(np.array(v, dtype=float) for v in (myop, myhi, mylo, mycl, myvol)))


def _read_wide(path):
    """Read the wide format that ships with the repository."""
    with open(path, encoding="latin-1") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in handle if line.strip()]
    stocks = np.array(header[1:])
    tday = np.array([int(float(row[0])) for row in rows], dtype=np.int64)
    prices = np.array([[float(v) for v in row[1:]] for row in rows], dtype=float)
    nan = np.full_like(prices, np.nan)
    return tday, stocks, nan, nan, nan, prices, nan


def main():
    input_file = INPUT_FILE
    with open(input_file, encoding="latin-1") as handle:
        header = handle.readline().rstrip("\n").split("\t")

    if len(header) > 2 and header[0].strip() == "Date":
        print("Export.txt is in wide format; op/hi/lo/vol will be NaN.")
        tday, stocks, op, hi, lo, cl, vol = _read_wide(input_file)
    else:
        mysym, mytday, myop, myhi, mylo, mycl, myvol = _read_long(input_file)

        # Since the single file consists of many symbols, we need to find the
        # unique set of symbols.
        stocks = np.unique(mysym)
        # Since the single file consists of many repeating sets of dates for
        # different symbols, we need to find the unique set of dates.
        tday = np.unique(mytday)

        op = np.full((len(tday), len(stocks)), np.nan)
        hi = np.full((len(tday), len(stocks)), np.nan)
        lo = np.full((len(tday), len(stocks)), np.nan)
        cl = np.full((len(tday), len(stocks)), np.nan)
        vol = np.full((len(tday), len(stocks)), np.nan)

        for s, stk in enumerate(stocks):
            # find the locations (indices) of the data with the current symbol.
            idx_a = np.flatnonzero(mysym == stk)
            # find the locations of the current set of dates.
            _common, idxt_a, idxt_b = intersect(mytday[idx_a], tday)
            op[idxt_b, s] = myop[idx_a[idxt_a]]
            hi[idxt_b, s] = myhi[idx_a[idxt_a]]
            lo[idxt_b, s] = mylo[idx_a[idxt_a]]
            cl[idxt_b, s] = mycl[idx_a[idxt_a]]
            vol[idxt_b, s] = myvol[idx_a[idxt_a]]

    savemat(OUTPUT_FILE,
            {"tday": tday.reshape(-1, 1), "stocks": stocks.reshape(-1, 1),
             "op": op, "hi": hi, "lo": lo, "cl": cl, "vol": vol})
    print("wrote %s  (%d dates x %d symbols)" % (OUTPUT_FILE, len(tday), len(stocks)))
    return tday, stocks, op, hi, lo, cl, vol


if __name__ == "__main__":
    main()
