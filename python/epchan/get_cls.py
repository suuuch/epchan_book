"""Port of the MATLAB ``getCls.m``.

Same as :func:`epchan.get_tday` but the prices are sorted by ascending date.
"""

import numpy as np

from .matlab_compat import excel_serial_to_yyyymmdd, sort_index, xlsread


def get_cls(filename):
    """Return the adjusted close prices of ``filename`` sorted by date."""
    num, _txt = xlsread(filename)
    tday = np.array([excel_serial_to_yyyymmdd(v) for v in num[:, 0]])
    cls = num[:, -1]
    _sorted_tday, sort_index_ = sort_index(tday)
    return cls[sort_index_]
