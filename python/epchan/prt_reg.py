"""Print the output of an ordinary least squares regression.

The MATLAB original relies on ``prt_reg.m``, a file that is *not* part of this
repository, but ``prt.m`` calls it for every regression result.  This module
provides the missing counterpart so that :func:`epchan.prt` works for the
``ols`` results as well.
"""

import sys

import numpy as np


def prt_reg(results, vnames=None, fid=None):
    """Print the results of an :func:`epchan.ols` regression."""
    if fid is None:
        fid = sys.stdout

    beta = np.asarray(results.beta).ravel()
    tstat = np.asarray(results.tstat).ravel()
    bstd = np.asarray(results.bstd).ravel()
    bint = np.asarray(results.bint).reshape(len(beta), 2)

    if vnames is None or len(vnames) == 0:
        names = ["x%d" % (i + 1) for i in range(len(beta))]
    else:
        names = [str(v) for v in vnames]

    nobs = results.nobs
    nvar = results.nvar

    fid.write("\n")
    fid.write("%-14s %12s %12s %10s %8s %12s %12s\n"
              % ("Variable", "Coefficient", "Std Error", "t-stat", "Prob(>t)",
                 "95% Lower", "95% Upper"))
    fid.write("%s\n" % ("-" * 80))
    for i, name in enumerate(names):
        prob = _t_sf(abs(tstat[i]), nobs - nvar)
        fid.write("%-14s %12.6f %12.6f %10.4f %8.4f %12.6f %12.6f\n"
                  % (name, beta[i], bstd[i], tstat[i], prob, bint[i, 0], bint[i, 1]))
    fid.write("\n")
    fid.write("R-squared          %12.6f\n" % results.rsqr)
    fid.write("R-bar-squared      %12.6f\n" % results.rbar)
    fid.write("Durbin-Watson stat %12.6f\n" % results.dw)
    fid.write("Observations       %12d\n" % nobs)


def _t_sf(t, dof):
    """Two sided p-value of a t statistic."""
    try:
        from scipy.stats import t as t_dist
    except ImportError:  # pragma: no cover - scipy is a hard dependency
        return float("nan")
    if dof <= 0:
        return float("nan")
    return float(2.0 * t_dist.sf(abs(t), dof))
