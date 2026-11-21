"""Port of the MATLAB ``smartsum.m`` written by Ernest Chan."""

import numpy as np

from .matlab_compat import first_non_singleton_axis


def smartsum(x, axis=None):
    """Sum along ``axis``, ignoring NaN and Inf.

    Slices that contain no finite value at all become ``NaN``.
    """
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    has_data = np.isfinite(x)
    xs = np.where(has_data, x, 0.0)
    y = xs.sum(axis=axis)
    all_bad = np.all(~has_data, axis=axis)
    return np.where(all_bad, np.nan, y)
