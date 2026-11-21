"""Port of the MATLAB ``lag1.m`` written by Ernest Chan.

``lag1`` shifts a matrix down by one row and pads the first row with ``NaN``
(or with ``''`` for character arrays).
"""

import numpy as np


def lag1(x):
    """Return ``x`` lagged by one observation (first row filled with ``NaN``)."""
    x = np.asarray(x)
    if x.ndim == 1:
        if x.dtype.kind in "US":
            empty = np.array([""], dtype=x.dtype)
        else:
            empty = np.array([np.nan])
        return np.concatenate([empty, x[:-1]])
    if x.dtype.kind in "US":
        empty = np.full((1,) + x.shape[1:], "", dtype=x.dtype)
    else:
        empty = np.full((1,) + x.shape[1:], np.nan, dtype=float)
    return np.vstack([empty, x[:-1]])
