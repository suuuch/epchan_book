"""Port of the MATLAB ``cadf.m`` written by James P. LeSage.

Computes the augmented Dickey-Fuller statistic of the residuals of a
cointegrating regression, allowing for deterministic polynomial trends.
"""

from dataclasses import dataclass

import numpy as np

from .cols import cols
from .lag import lag
from .matlab_compat import detrend, left_divide
from .rows import rows
from .rztcrit import rztcrit
from .tdiff import tdiff
from .trimr import trimr


@dataclass
class CadfResults:
    """The results structure returned by :func:`cadf` (same fields as MATLAB)."""

    meth: str = "cadf"
    alpha: float = np.nan
    adf: float = np.nan
    crit: np.ndarray = None
    nvar: int = 0
    nlag: int = 0


def cadf(y, x, p, l):
    """Augmented Dickey-Fuller test on the residuals of ``y`` regressed on ``x``.

    ``y`` is the dependent variable (a vector), ``x`` the matrix of
    explanatory variables, ``p`` the order of the time polynomial of the null
    hypothesis and ``l`` the number of lagged differences of the residuals.
    """
    if p < -1:
        raise ValueError("p cannot be < -1 in cadf")

    y = np.asarray(y, dtype=float).ravel()
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)

    nobs = rows(x)
    if nobs - (2 * l) + 1 < 1:
        raise ValueError("nlags is too large in cadf; negative degrees of freedom")

    y = detrend(y, p)
    x = detrend(x, p)

    b = np.linalg.inv(x.T @ x) @ (x.T @ y)
    r = y - x @ b

    dep = tdiff(r, 1)
    dep = trimr(dep, 1, 0)

    z = trimr(lag(r, 1), 1, 0)
    for k in range(1, l + 1):
        z = np.hstack([z, lag(dep, k)])
    z = trimr(z, l, 0)
    dep = trimr(dep, l, 0)

    beta = left_divide(detrend(z, 0), detrend(dep, 0))
    res = detrend(dep, 0) - detrend(z, 0) @ beta

    so = float(res.ravel() @ res.ravel()) / (rows(dep) - cols(z))
    var_cov = so * np.linalg.inv(z.T @ z)

    results = CadfResults()
    results.alpha = beta[0, 0]
    results.adf = beta[0, 0] / np.sqrt(var_cov[0, 0])
    results.crit = rztcrit(nobs, cols(x), p)
    results.nlag = l
    results.nvar = cols(x)
    return results
