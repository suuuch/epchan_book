"""Port of the MATLAB ``lag.m`` written by James P. LeSage.

``lag`` pads the top of the matrix with a constant (0 by default) and drops
the same number of rows at the bottom.  It is *not* the same as :func:`lag1`,
which pads with ``NaN``.
"""

import numpy as np

from .cols import cols


def lag(x, n=1, v=0.0):
    """Return ``x`` lagged by ``n`` observations, padded with ``v``.

    ``n <= 0`` returns an empty array, as in MATLAB.

    A one dimensional input gives a one dimensional result here, whereas
    MATLAB always returns a matrix (a Python 1-D array is closer to a MATLAB
    column vector in the rest of this package).
    """
    x = np.asarray(x)
    if n < 1:
        return np.empty((0,) + x.shape[1:], dtype=x.dtype)
    pad = np.full((n, cols(x)), v, dtype=float)
    if x.ndim == 1:
        pad = pad[:, 0]
        return np.concatenate([pad, x[:x.shape[0] - n]])
    return np.vstack([pad, x[:x.shape[0] - n]])
