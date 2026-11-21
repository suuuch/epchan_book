"""Port of the MATLAB ``cols.m``: number of columns of a matrix."""

import numpy as np


def cols(x):
    """Return the number of columns of ``x``.

    A one dimensional array is treated as a column vector, so ``cols`` returns
    ``1`` for it, just like MATLAB does for ``n x 1`` vectors.
    """
    shape = np.shape(x)
    if len(shape) < 2:
        return 1
    return shape[1]
