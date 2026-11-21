"""Port of the MATLAB ``smartstd1.m`` written by Ernest Chan.

Standard deviation along ``axis`` ignoring NaN and Inf.  As in the original
this normalises by ``N-1`` (MATLAB's ``std`` convention), unlike
:func:`epchan.smartstd` which normalises by ``N``.
"""

import numpy as np

from .matlab_compat import first_non_singleton_axis


def smartstd1(x, axis=None):
    """Standard deviation along ``axis``, ignoring NaN and Inf (normalised by N-1).

    The MATLAB original passes no ``dim`` to ``std``, so it always reduces
    along the first non singleton dimension while masking along ``dim``; that
    mismatch is a latent bug of the original.  This port reduces and masks
    along the same ``axis`` so the function behaves consistently.
    """
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    has_data = np.isfinite(x)
    xs = np.where(has_data, x, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        y = xs.std(axis=axis, ddof=1)
    all_bad = np.all(~has_data, axis=axis)
    return np.where(all_bad, np.nan, y)
