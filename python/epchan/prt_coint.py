"""Port of the MATLAB ``prt_coint.m`` written by James P. LeSage.

Prints the output of the cointegration tests (``adf``, ``cadf``, ``johansen``
and ``phillips``).
"""

import sys

import numpy as np

from .mprint import mprint


def _write(fid, text):
    fid.write(text)


def prt_coint(result, vnames=None, fid=None):
    """Print the results of a cointegration test.

    ``result`` is the structure returned by :func:`epchan.cadf` (or by the
    ``adf``/``phillips``/``johansen`` tests), ``vnames`` an optional list with
    the names of the variables and ``fid`` the file object to write to.
    """
    if fid is None:
        fid = sys.stdout

    nflag = 1 if (vnames is not None and len(vnames) > 0) else 0

    meth = getattr(result, "meth", None)
    if meth == "johansen":
        return _prt_johansen(result, vnames, fid, nflag)
    if meth == "adf":
        return _prt_adf(result, vnames, fid, nflag)
    if meth == "cadf":
        return _prt_cadf(result, vnames, fid, nflag)
    if meth == "phillips":
        return _prt_phillips(result, vnames, fid, nflag)
    raise ValueError("results structure not known by prt_coint function")


def _generic_names(count):
    return ["variable   %d" % (i + 1) for i in range(count)]


def _prt_cadf(result, vnames, fid, nflag):
    if nflag == 0:
        vname = _generic_names(2)
    else:
        if len(vnames) != 2:
            raise ValueError("Wrong # of variable names in prt_coint -- check vnames argument")
        vname = [str(v)[:16] for v in vnames]

    _write(fid, "\n Augmented DF test for co-integration")
    _write(fid, " variables: %30s  \n" % ("%s,%s" % (vname[0], vname[1])))

    mprint(np.array([[result.adf, result.nlag, result.alpha]]),
           {"cnames": ["CADF t-statistic", "# of lags", "AR(1) estimate"],
            "fmt": ["%16.8f", "%10d", "%16.6f"],
            "fid": fid})

    mprint(np.asarray(result.crit).ravel()[0:3].reshape(1, 3),
           {"cnames": ["1% Crit Value", "5% Crit Value", "10% Crit Value"],
            "fmt": "%16.3f",
            "fid": fid})


def _prt_adf(result, vnames, fid, nflag):
    if nflag == 0:
        vname = _generic_names(1)
    else:
        vname = [str(vnames[0])[:16]]

    _write(fid, "\nAugmented DF test for unit root variable: %30s \n" % vname[0])

    mprint(np.array([[result.adf, result.nlag, result.alpha]]),
           {"cnames": ["ADF t-statistic", "# of lags", "AR(1) estimate"],
            "fmt": ["%16.6f", "%10d", "%16.6f"],
            "fid": fid})

    mprint(np.asarray(result.crit).ravel()[0:3].reshape(1, 3),
           {"cnames": ["1% Crit Value", "5% Crit Value", "10% Crit Value"],
            "fmt": "%16.3f",
            "fid": fid})


def _prt_phillips(result, vnames, fid, nflag):
    if nflag == 0:
        vname = _generic_names(2)
    else:
        if len(vnames) != 2:
            raise ValueError("Wrong # of variable names in prt_coint -- check vnames argument")
        vname = [str(v)[:16] for v in vnames]

    _write(fid, "\n Phillips-Peron test for co-integration")
    _write(fid, " variables: %30s  \n" % ("%s,%s" % (vname[0], vname[1])))

    mprint(np.array([[result.pstat, result.nlag, result.alpha]]),
           {"cnames": ["Phillips-Peron statistic", "# of lags", "AR(1) estimate"],
            "fmt": ["%16.8f", "%10d", "%16.6f"],
            "fid": fid})

    mprint(np.asarray(result.crit).ravel()[0:3].reshape(1, 3),
           {"cnames": ["1% Crit Value", "5% Crit Value", "10% Crit Value"],
            "fmt": "%16.3f",
            "fid": fid})


def _as_column(values):
    """Return ``values`` as an ``(n, 1)`` matrix (no-op for a 2-D input)."""
    values = np.asarray(values, dtype=float)
    if values.ndim == 1:
        values = values.reshape(-1, 1)
    return values


def _prt_johansen(result, vnames, fid, nflag):
    eig = np.asarray(result.eig)
    # MATLAB's ``[nvar junk] = size(result.eig)``
    nvar = eig.shape[0]
    index = np.asarray(result.ind).ravel()

    if nflag == 1:
        vnames = np.asarray(vnames)
        if vnames.shape[0] != nvar:
            _write(fid, "Wrong # of variable names in prt_coint -- check vnames argument \n")
            _write(fid, "will use generic variable names \n")
            nflag = 0
        else:
            vname = [str(vnames[i - 1]) for i in index]
    if nflag == 0:
        vname = ["variable   %d" % i for i in index]

    rname = ["NULL:"]
    for i in range(nvar):
        rname.append("r <= %d   %s" % (i, vname[i]))

    _write(fid, "\n Johansen MLE estimates \n")
    # MATLAB: prtmat = [result.lr1 result.cvt]
    mprint(np.hstack([_as_column(result.lr1), _as_column(result.cvt)]),
           {"cnames": ["Trace Statistic", "Crit 90%", "Crit 95%", "Crit 99%"],
            "rnames": rname,
            "fmt": "%16.3f",
            "fid": fid})
    mprint(np.hstack([_as_column(result.lr2), _as_column(result.cvm)]),
           {"cnames": ["Eigen Statistic", "Crit 90%", "Crit 95%", "Crit 99%"],
            "rnames": rname,
            "fmt": "%16.3f",
            "fid": fid})
