"""Port of the MATLAB ``smartmean1.m`` written by Ernest Chan.

Same idea as :func:`epchan.smartmean` but written by the author of the book;
it behaves identically for 1- and 2-D input.
"""

import numpy as np

from .matlab_compat import first_non_singleton_axis


def smartmean1(x, axis=None):
    """Mean value along ``axis``, ignoring NaN and Inf."""
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    has_data = np.isfinite(x)
    xs = np.where(has_data, x, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        y = xs.sum(axis=axis) / has_data.sum(axis=axis)
    all_bad = np.all(~has_data, axis=axis)
    return np.where(all_bad, np.nan, y)
