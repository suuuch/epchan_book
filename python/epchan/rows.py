"""Port of the MATLAB ``rows.m``: number of rows of a matrix."""

import numpy as np


def rows(x):
    """Return the number of rows of ``x``."""
    return np.shape(x)[0]
