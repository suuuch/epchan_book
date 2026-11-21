"""Port of the MATLAB ``fillMissingData.m`` written by Ernest Chan."""

import numpy as np


def fill_missing_data(prices):
    """Fill the NaN/Inf entries of a 2-D array with the previous value.

    The first row is left untouched, exactly as in the MATLAB code.
    """
    filled = np.array(prices, dtype=float, copy=True)
    for t in range(1, filled.shape[0]):
        miss_data = ~np.isfinite(filled[t, :])
        filled[t, miss_data] = filled[t - 1, miss_data]
    return filled
