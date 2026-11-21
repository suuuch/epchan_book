"""Port of the MATLAB ``backshift.m`` written by Ernest Chan.

``backshift`` shifts a matrix *forward* in time: the first ``day`` rows become
``NaN`` and the last ``day`` rows are dropped, so the number of rows is
unchanged.
"""

import numpy as np


def backshift(day, x):
    """Return ``x`` shifted forward by ``day`` rows (first rows are ``NaN``)."""
    x = np.asarray(x)
    day = int(day)
    if day < 0:
        raise ValueError("day = %d < 0, error!" % day)
    n = x.shape[0]
    body = x[:max(n - day, 0)]
    if x.ndim == 1:
        return np.concatenate([np.full(day, np.nan), body])
    pad = np.full((day,) + x.shape[1:], np.nan, dtype=float)
    return np.vstack([pad, body])
