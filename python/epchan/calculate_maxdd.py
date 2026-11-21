"""Port of the MATLAB ``calculateMaxDD.m`` written by Ernest Chan.

Maximum drawdown and maximum drawdown duration of a series of *cumulative
compounded* returns.
"""

import numpy as np


def calculate_maxdd(cumret):
    """Return ``(maxDD, maxDDD)``: the maximum drawdown and its longest duration."""
    cumret = np.asarray(cumret, dtype=float).ravel()

    highwatermark = np.zeros_like(cumret)
    drawdown = np.zeros_like(cumret)
    drawdownduration = np.zeros_like(cumret)

    for t in range(1, len(cumret)):
        highwatermark[t] = max(highwatermark[t - 1], cumret[t])
        drawdown[t] = (1.0 + highwatermark[t]) / (1.0 + cumret[t]) - 1.0
        if drawdown[t] == 0:
            drawdownduration[t] = 0
        else:
            drawdownduration[t] = drawdownduration[t - 1] + 1

    max_dd = drawdown.max() if drawdown.size else np.nan
    max_ddd = drawdownduration.max() if drawdownduration.size else np.nan
    return max_dd, max_ddd
