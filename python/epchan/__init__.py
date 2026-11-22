"""Python port of the MATLAB source of Ernest P. Chan's book

    "Quantitative Trading: How to Build Your Own Algorithmic Trading Business"

Python 移植版本，源自 Ernest P. Chan 的著作

    《Quantitative Trading: How to Build Your Own Algorithmic Trading Business》

Every function in this package has a 1:1 counterpart in the original MATLAB
code (the ``.m`` files that live in the root of the repository).  The module
names are the snake_case version of the MATLAB file names, e.g. the MATLAB
``calculateMaxDD.m`` becomes :mod:`epchan.calculate_maxdd`.

本包中的每个函数在原始 MATLAB 代码（仓库根目录下的 ``.m`` 文件）中都有
一一对应的实现。模块名是 MATLAB 文件名的 snake_case 写法，例如 MATLAB 的
``calculateMaxDD.m`` 变为 :mod:`epchan.calculate_maxdd`。

Conventions used throughout the package
---------------------------------------

全包通用的约定
--------------

* MATLAB is 1-based, Python is 0-based.  All *index* arithmetic has been
  translated, so the returned values are identical to the MATLAB originals.
  MATLAB 从 1 开始编号，Python 从 0 开始编号。所有*下标*运算都已相应转换，
  因此返回值与 MATLAB 原版完全一致。
* MATLAB's ``dim`` argument is exposed as a **0-based** numpy ``axis``
  argument.  MATLAB ``dim=1`` (down the rows) is Python ``axis=0``.
  MATLAB 的 ``dim`` 参数以**从 0 开始**的 numpy ``axis`` 参数呈现。
  MATLAB 的 ``dim=1``（沿行方向）对应 Python 的 ``axis=0``。
* MATLAB structures are replaced by small dataclasses with the very same
  field names (``results.beta``, ``results.adf``, ...).
  MATLAB 的结构体被替换为字段名完全相同的小型 dataclass
  （``results.beta``、``results.adf`` 等）。

Exported helpers
----------------

导出的辅助函数
--------------

* **Data and matrix helpers** -- ``assert_``, ``cols``, ``rows``, ``get_cls``,
  ``fill_missing_data``.
  **数据与矩阵辅助函数** -- ``assert_``、``cols``、``rows``、``get_cls``、
  ``fill_missing_data``。
* **Series shifting and differencing** -- ``backshift``, ``fwdshift``, ``lag``,
  ``lag1``, ``tdiff``, ``trimr``.
  **序列移位与差分** -- ``backshift``、``fwdshift``、``lag``、``lag1``、
  ``tdiff``、``trimr``。
* **Trading calendar** -- ``get_tday``, ``is_last_trading_day_of_month``.
  **交易日历** -- ``get_tday``、``is_last_trading_day_of_month``。
* **Statistics and printing** -- ``beta_inv``, ``beta_pdf``, ``tdis_inv``,
  ``smartcov``, ``smartmean``, ``smartmean1``, ``smartstd``, ``smartstd1``,
  ``smartsum``, ``mprint``.
  **统计与打印** -- ``beta_inv``、``beta_pdf``、``tdis_inv``、``smartcov``、
  ``smartmean``、``smartmean1``、``smartstd``、``smartstd1``、``smartsum``、
  ``mprint``。
* **Econometric models and unit-root tests** -- ``cadf``, ``CadfResults``,
  ``ols``, ``OlsResults``, ``rztcrit``.
  **计量模型与单位根检验** -- ``cadf``、``CadfResults``、``ols``、
  ``OlsResults``、``rztcrit``。
* **Reporting and performance** -- ``prt``, ``prt_coint``, ``prt_reg``,
  ``calculate_maxdd``.
  **报告与绩效** -- ``prt``、``prt_coint``、``prt_reg``、``calculate_maxdd``。
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
