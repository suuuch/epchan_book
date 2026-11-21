"""Python port of the MATLAB source of Ernest P. Chan's book

    "Quantitative Trading: How to Build Your Own Algorithmic Trading Business"

Every function in this package has a 1:1 counterpart in the original MATLAB
code (the ``.m`` files that live in the root of the repository).  The module
names are the snake_case version of the MATLAB file names, e.g. the MATLAB
``calculateMaxDD.m`` becomes :mod:`epchan.calculate_maxdd`.

Conventions used throughout the package
---------------------------------------

* MATLAB is 1-based, Python is 0-based.  All *index* arithmetic has been
  translated, so the returned values are identical to the MATLAB originals.
* MATLAB's ``dim`` argument is exposed as a **0-based** numpy ``axis``
  argument.  MATLAB ``dim=1`` (down the rows) is Python ``axis=0``.
* MATLAB structures are replaced by small dataclasses with the very same
  field names (``results.beta``, ``results.adf``, ...).
"""

from .assert_ import assert_
from .backshift import backshift
from .beta_inv import beta_inv
from .beta_pdf import beta_pdf
from .cadf import CadfResults, cadf
from .calculate_maxdd import calculate_maxdd
from .cols import cols
from .fill_missing_data import fill_missing_data
from .fwdshift import fwdshift
from .get_cls import get_cls
from .get_tday import get_tday
from .is_last_trading_day_of_month import is_last_trading_day_of_month
from .lag import lag
from .lag1 import lag1
from .mprint import mprint
from .ols import OlsResults, ols
from .prt import prt
from .prt_coint import prt_coint
from .prt_reg import prt_reg
from .rztcrit import rztcrit
from .rows import rows
from .smartcov import smartcov
from .smartmean import smartmean
from .smartmean1 import smartmean1
from .smartstd import smartstd
from .smartstd1 import smartstd1
from .smartsum import smartsum
from .tdiff import tdiff
from .tdis_inv import tdis_inv
from .trimr import trimr

__all__ = [
    "assert_",
    "backshift",
    "beta_inv",
    "beta_pdf",
    "cadf",
    "CadfResults",
    "calculate_maxdd",
    "cols",
    "fill_missing_data",
    "fwdshift",
    "get_cls",
    "get_tday",
    "is_last_trading_day_of_month",
    "lag",
    "lag1",
    "mprint",
    "ols",
    "OlsResults",
    "prt",
    "prt_coint",
    "prt_reg",
    "rztcrit",
    "rows",
    "smartcov",
    "smartmean",
    "smartmean1",
    "smartstd",
    "smartstd1",
    "smartsum",
    "tdiff",
    "tdis_inv",
    "trimr",
]
