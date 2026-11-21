"""Port of the MATLAB ``smartmean.m`` (mean ignoring NaN and Inf)."""

import numpy as np

from .matlab_compat import first_non_singleton_axis


def smartmean(x, axis=None):
    """Average of the finite elements of ``x`` along ``axis``.

    Columns (or slices) that contain no finite value at all become ``NaN``.
    ``axis`` is a 0-based numpy axis; when omitted the first non singleton
    axis is used, exactly like MATLAB.
    """
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    has_data = np.isfinite(x)
    xs = np.where(has_data, x, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        y = xs.sum(axis=axis) / has_data.sum(axis=axis)
    all_bad = np.all(~has_data, axis=axis)
    return np.where(all_bad, np.nan, y)
