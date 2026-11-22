"""Port of the MATLAB ``smartstd1.m`` written by Ernest Chan.

PURPOSE: y = smartstd(x, dim) -- std along dimension dim, ignoring NaN and
         Inf.
         Written by Ernest Chan, author of "Quantitative Trading: How to
         Start Your Own Algorithmic Trading Business"
         (ernest@epchan.com, www.epchan.com).
用途: y = smartstd(x, dim) -- 沿 dim 维求标准差，忽略 NaN 和 Inf。
      编写者：Ernest Chan
      著有“Quantitative Trading: How to Start Your Own Algorithmic Trading
      Business”一书（ernest@epchan.com，www.epchan.com）。

Standard deviation along ``axis`` ignoring NaN and Inf.  As in the original
this normalises by ``N-1`` (MATLAB's ``std`` convention), unlike
:func:`epchan.smartstd` which normalises by ``N``.
沿 ``axis`` 维求标准差，忽略 NaN 和 Inf。与原版一样，它按 ``N-1``
归一化（MATLAB ``std`` 的惯例），而 :func:`epchan.smartstd` 按 ``N``
归一化。
"""

import numpy as np

from .matlab_compat import first_non_singleton_axis


def smartstd1(x, axis=None):
    """Standard deviation along ``axis``, ignoring NaN and Inf (normalised by N-1).

    The MATLAB original passes no ``dim`` to ``std``, so it always reduces
    along the first non singleton dimension while masking along ``dim``; that
    mismatch is a latent bug of the original.  This port reduces and masks
    along the same ``axis`` so the function behaves consistently.

    沿 ``axis`` 维求标准差，忽略 NaN 和 Inf（按 N-1 归一化）。

    MATLAB 原版在调用 ``std`` 时没有传入 ``dim``，因此它总是沿第一个
    非单例维度求约简，却沿 ``dim`` 做掩码；这种不一致是原版的潜在缺陷。
    本移植版本在求约简和做掩码时使用同一个 ``axis``，使函数行为保持一致。
    """
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    has_data = np.isfinite(x)
    xs = np.where(has_data, x, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        y = xs.std(axis=axis, ddof=1)
    all_bad = np.all(~has_data, axis=axis)
    return np.where(all_bad, np.nan, y)
