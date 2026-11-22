"""Port of the MATLAB ``smartsum.m`` written by Ernest Chan.

PURPOSE: y = smartsum(x, dim) -- sum along dimension dim, ignoring NaN.
         Written by Ernest Chan, author of "Quantitative Trading: How to
         Start Your Own Algorithmic Trading Business"
         (ernest@epchan.com, www.epchan.com).
用途: y = smartsum(x, dim) -- 沿 dim 维求和，忽略 NaN。
      编写者：Ernest Chan
      著有“Quantitative Trading: How to Start Your Own Algorithmic Trading
      Business”一书（ernest@epchan.com，www.epchan.com）。
"""

import numpy as np

from .matlab_compat import first_non_singleton_axis


def smartsum(x, axis=None):
    """Sum along ``axis``, ignoring NaN and Inf.

    Slices that contain no finite value at all become ``NaN``.

    沿 ``axis`` 维求和，忽略 NaN 和 Inf。

    完全不含有限值的切片会变成 ``NaN``。
    """
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    has_data = np.isfinite(x)
    xs = np.where(has_data, x, 0.0)
    y = xs.sum(axis=axis)
    all_bad = np.all(~has_data, axis=axis)
    return np.where(all_bad, np.nan, y)
