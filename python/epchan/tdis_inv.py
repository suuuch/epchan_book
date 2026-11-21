"""Port of the MATLAB ``tdis_inv.m`` written by Anders Holtsberg.

Inverse of the cumulative distribution function (quantile) of Student's t
distribution with ``a`` degrees of freedom.
"""

import numpy as np

from .beta_inv import beta_inv


def tdis_inv(p, a):
    """Return the t quantile(s) for the probabilities ``p`` and ``a`` degrees of freedom."""
    p = np.asarray(p, dtype=float)
    s = p < 0.5
    p = p + (1.0 - 2.0 * p) * s
    p = 1.0 - 2.0 * (1.0 - p)
    x = beta_inv(p, 0.5, a / 2.0)
    x = x * a / (1.0 - x)
    x = (1.0 - 2.0 * s) * np.sqrt(x)
    return x
