"""Port of the MATLAB ``beta_inv.m`` written by Anders Holtsberg.

Inverse of the cumulative distribution function (quantile) of the beta
distribution, computed with the very same Newton iteration as the original.
"""

import numpy as np
from scipy.stats import beta as beta_dist

from .beta_pdf import beta_pdf

_EPS = np.finfo(float).eps


def beta_inv(p, a, b):
    """Quantile of the ``beta(a, b)`` distribution for each probability in ``p``."""
    p = np.asarray(p, dtype=float)
    if np.any(np.asarray(a) <= 0) or np.any(np.asarray(b) <= 0):
        raise ValueError("beta_inv parameter a or b is nonpositive")
    if np.any(np.abs(2.0 * p - 1.0) > 1.0):
        raise ValueError("beta_inv: A probability should be 0<=p<=1")

    x = np.full(p.shape, a / (a + b), dtype=float)
    dx = np.ones_like(x)
    # The original MATLAB code has no iteration limit; a guard is added here so
    # that a pathological input cannot hang the program.
    for _ in range(200):
        if not np.any(np.abs(dx) > 256.0 * _EPS * np.maximum(x, 1.0)):
            break
        x_eval = np.clip(x, np.finfo(float).tiny, 1.0 - np.finfo(float).eps)
        dx = (beta_dist.cdf(x_eval, a, b) - p) / beta_pdf(x_eval, a, b)
        x = x - dx
        # The original line is 'x = x + (dx - x)/2 .* (x<0)'.
        x = x + (dx - x) / 2.0 * (x < 0)
    return x
