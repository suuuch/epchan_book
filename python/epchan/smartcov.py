"""Port of the MATLAB ``smartcov.m``.

Covariance of the finite elements.  Rows are observations, columns are
variables.  Like :func:`epchan.smartstd` the normalisation is by ``N`` and not
by ``N-1``, and NaN/Inf entries are ignored instead of being propagated.
"""

import numpy as np

from .smartmean import smartmean


def smartcov(x):
    """Covariance matrix of the columns of ``x``.

    The MATLAB original fills a nested ``for m``/``for n`` loop with

        y(m, n) = smartmean(xc(:, m) .* xc(:, n), 1)

    which is the average of the products over the rows where *both* entries
    are finite.  That is computed here with two matrix products: the numerator
    is ``xc0.T @ xc0`` (the non finite products replaced by zero) and the
    denominator is the number of valid pairs, ``M.T @ M``.  The result is
    numerically identical and much faster.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)

    nvar = x.shape[1]
    y = np.full((nvar, nvar), np.nan)

    # Columns that are not entirely NaN take part in the computation.
    goodstk = np.flatnonzero(~np.all(np.isnan(x), axis=0))

    xc = np.full(x.shape, np.nan)
    xg = x[:, goodstk]
    xc[:, goodstk] = xg - smartmean(xg, axis=0)

    xc = xc[:, goodstk]
    valid = np.isfinite(xc)
    xc0 = np.where(valid, xc, 0.0)
    numerator = xc0.T @ xc0
    denominator = valid.T.astype(float) @ valid.astype(float)

    with np.errstate(invalid="ignore", divide="ignore"):
        sub = numerator / denominator
    sub[denominator == 0] = np.nan

    y[np.ix_(goodstk, goodstk)] = sub
    return y
