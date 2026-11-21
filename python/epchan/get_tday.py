"""Port of the MATLAB ``getTday.m``.

Reads a spreadsheet whose first column holds the trading days (as Excel day
numbers) and whose last column holds the adjusted close prices.
"""

import numpy as np

from .matlab_compat import excel_serial_to_yyyymmdd, xlsread


def get_tday(filename):
    """Return ``(tday, adjcls)`` for the spreadsheet ``filename``.

    ``tday`` is an array of ``yyyymmdd`` integers, ``adjcls`` the adjusted
    close prices (last column of the spreadsheet).
    """
    num, _txt = xlsread(filename)
    tday = np.array([excel_serial_to_yyyymmdd(v) for v in num[:, 0]])
    adjcls = num[:, -1]
    return tday, adjcls
