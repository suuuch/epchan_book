"""Port of the MATLAB ``beta_pdf.m`` written by Anders Holtsberg.

Probability density function of the beta distribution.
"""

import numpy as np
from scipy.special import beta as beta_


def beta_pdf(x, a, b):
    """Density of the ``beta(a, b)`` distribution evaluated at ``x``."""
    x = np.asarray(x, dtype=float)
    if np.any(np.asarray(a) <= 0) or np.any(np.asarray(b) <= 0):
        raise ValueError("Parameter a or b is nonpositive")

    pdf = np.zeros_like(x, dtype=float)
    inside = np.isfinite(x) & (x >= 0) & (x <= 1)
    xi = x[inside]
    with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
        pdf[inside] = xi ** (a - 1.0) * (1.0 - xi) ** (b - 1.0) / beta_(a, b)
    return pdf
