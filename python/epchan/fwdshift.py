"""Port of the MATLAB ``fwdshift.m`` written by Ernest Chan.

``fwdshift`` shifts a matrix *backward* in time: the first ``day`` rows are
dropped and ``day`` ``NaN`` rows are appended at the bottom.
"""

import numpy as np

from .assert_ import assert_


def fwdshift(day, x):
    """Return ``x`` shifted backward by ``day`` rows (last rows are ``NaN``)."""
    x = np.asarray(x)
    day = int(day)
    assert_(day >= 0)
    pad = np.full((day,) + x.shape[1:], np.nan, dtype=float)
    body = x[day:]
    if x.ndim == 1:
        return np.concatenate([body, np.full(day, np.nan)])
    return np.vstack([body, pad])
