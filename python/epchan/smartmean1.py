"""Port of the MATLAB ``smartmean1.m`` written by Ernest Chan.

PURPOSE: y = smartmean(x, dim) -- mean value along dimension dim, ignoring
         NaN.
         Written by Ernest Chan, author of "Quantitative Trading: How to
         Start Your Own Algorithmic Trading Business"
         (ernest@epchan.com, www.epchan.com).
用途: y = smartmean(x, dim) -- 沿 dim 维求均值，忽略 NaN。
      编写者：Ernest Chan
      著有“Quantitative Trading: How to Start Your Own Algorithmic Trading
      Business”一书（ernest@epchan.com，www.epchan.com）。

Same idea as :func:`epchan.smartmean` but written by the author of the book;
it behaves identically for 1- and 2-D input.
与 :func:`epchan.smartmean` 思路相同，但由本书作者编写；
对 1 维和 2 维输入其行为完全一致。
"""

import numpy as np

from .matlab_compat import first_non_singleton_axis


def smartmean1(x, axis=None):
    """Mean value along ``axis``, ignoring NaN and Inf.

    沿 ``axis`` 维求均值，忽略 NaN 和 Inf。
    """
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    has_data = np.isfinite(x)
    xs = np.where(has_data, x, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        y = xs.sum(axis=axis) / has_data.sum(axis=axis)
    all_bad = np.all(~has_data, axis=axis)
    # Set y to NaN if all entries are NaN's.
    # 如果所有元素都是 NaN，则将 y 设为 NaN。
    return np.where(all_bad, np.nan, y)
