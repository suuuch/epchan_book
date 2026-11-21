"""Port of the MATLAB ``smartstd.m``.

Standard deviation of the finite elements; unlike MATLAB's ``std`` it
normalises by ``N`` and not by ``N-1``.
"""

import numpy as np

from .matlab_compat import first_non_singleton_axis
from .smartmean import smartmean


def smartstd(x, axis=None):
    """Standard deviation along ``axis``, ignoring NaN and Inf (normalised by N)."""
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    mean = smartmean(x, axis=axis)
    # Broadcast the mean back over the reduced axis.
    shape = list(x.shape)
    shape.pop(axis)
    xc = x - np.asarray(mean).reshape(shape)
    return np.sqrt(smartmean(np.conj(xc) * xc, axis=axis))
