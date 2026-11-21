"""Port of the MATLAB ``prt.m`` written by James P. LeSage.

``prt`` is a thin wrapper that looks at the ``meth`` field of a results
structure and calls the matching printing routine.
"""

import sys

from .prt_coint import prt_coint
from .prt_reg import prt_reg

#: The methods understood by ``prt``.
_COINT_METHODS = ("johansen", "adf", "cadf", "phillips")
_REG_METHODS = ("arma", "boxcox", "boxcox2", "hwhite", "lad", "logit", "mlogit",
                "nwest", "ols", "olsc", "olsar1", "olst", "probit", "ridge",
                "robust", "theil", "tobit", "tsls")


def prt(results, vnames=None, fid=None):
    """Print a results structure.

    ``results`` is the structure returned by one of the econometric helpers
    (``ols``, ``cadf``, ...), ``vnames`` an optional list of variable names
    and ``fid`` the file object the output is written to.
    """
    if fid is None:
        fid = sys.stdout

    meth = getattr(results, "meth", None)
    if meth is None:
        raise ValueError("prt: requires a structure input")

    if meth in _COINT_METHODS:
        prt_coint(results, vnames, fid)
    elif meth in _REG_METHODS:
        prt_reg(results, vnames, fid)
    else:
        raise ValueError("results structure not known by prt function")
