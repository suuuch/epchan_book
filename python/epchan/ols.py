"""Port of the MATLAB ``ols.m`` written by James P. LeSage (and Barry Dillon).

Ordinary least squares regression.
"""

from dataclasses import dataclass

import numpy as np

from .tdis_inv import tdis_inv


@dataclass
class OlsResults:
    """The results structure returned by :func:`ols` (same fields as MATLAB)."""

    meth: str = "ols"
    y: np.ndarray = None
    nobs: int = 0
    nvar: int = 0
    beta: np.ndarray = None
    yhat: np.ndarray = None
    resid: np.ndarray = None
    sige: float = np.nan
    bstd: np.ndarray = None
    tstat: np.ndarray = None
    bint: np.ndarray = None
    rsqr: float = np.nan
    rbar: float = np.nan
    dw: float = np.nan


def ols(y, x):
    """Least squares regression of ``y`` on ``x``.

    ``y`` is a vector of ``nobs`` observations and ``x`` an ``(nobs x nvar)``
    matrix of explanatory variables.
    """
    y = np.asarray(y, dtype=float).ravel().reshape(-1, 1)
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)

    nobs, nvar = x.shape
    if nobs != y.size:
        raise ValueError("x and y must have same # obs in ols")

    results = OlsResults(y=y, nobs=nobs, nvar=nvar)

    if nobs < 10000:
        # QR decomposition, like the original code.
        _q, r = np.linalg.qr(x, mode="reduced")
        xpxi = np.linalg.inv(r.T @ r)
    else:
        xpxi = np.linalg.inv(x.T @ x)

    results.beta = xpxi @ (x.T @ y)
    results.yhat = x @ results.beta
    results.resid = y - results.yhat
    sigu = float(results.resid.ravel() @ results.resid.ravel())
    results.sige = sigu / (nobs - nvar)
    # ``tmp`` is a column vector, like MATLAB's ``sige*diag(xpxi)``.
    tmp = (results.sige * np.diag(xpxi)).reshape(-1, 1)
    sigb = np.sqrt(tmp)
    results.bstd = sigb
    tcrit = -tdis_inv(0.025, nobs)
    results.bint = np.column_stack([results.beta - tcrit * sigb,
                                    results.beta + tcrit * sigb])
    results.tstat = results.beta / np.sqrt(tmp)
    ym = y - y.mean()
    rsqr1 = sigu
    rsqr2 = float(ym.ravel() @ ym.ravel())
    results.rsqr = 1.0 - rsqr1 / rsqr2
    rsqr1 = rsqr1 / (nobs - nvar)
    rsqr2 = rsqr2 / (nobs - 1.0)
    if rsqr2 != 0:
        results.rbar = 1.0 - (rsqr1 / rsqr2)
    else:
        results.rbar = results.rsqr
    ediff = results.resid[1:] - results.resid[:-1]
    results.dw = float(ediff.ravel() @ ediff.ravel()) / sigu
    return results
