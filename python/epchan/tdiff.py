"""Port of the MATLAB ``tdiff.m`` written by James P. LeSage.

Produces ``x(t) - x(t-k)``; the first ``k`` observations are zero.
"""

import numpy as np


def tdiff(x, k):
    """Return the ``k``-period difference of ``x``.

    The shape of ``x`` is preserved: a vector stays a vector, a matrix stays a
    matrix, exactly like the MATLAB function.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim > 2:
        raise ValueError("tdiff expects a vector or a matrix")
    if k == 0:
        return x.copy()

    dmat = np.zeros_like(x)
    dmat[k:] = x[k:] - x[:-k]
    return dmat
