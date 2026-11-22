"""Port of the MATLAB ``smartstd.m``.

PURPOSE: SMARTSTD -- standard deviation of finite elements.
         Same as STD except that it ignores NaN and Inf instead of
         propagating them.
         Normalizes by N, not N-1.
用途: SMARTSTD -- 有限元素的标准差。
      与 STD 相同，但它会忽略 NaN 和 Inf，而不是传播它们。
      按 N 归一化，而不是 N-1。

Standard deviation of the finite elements; unlike MATLAB's ``std`` it
normalises by ``N`` and not by ``N-1``.
有限元素的标准差；与 MATLAB 的 ``std`` 不同，它按 ``N`` 归一化，
而不是 ``N-1``。
"""

import numpy as np

from .matlab_compat import first_non_singleton_axis
from .smartmean import smartmean


def smartstd(x, axis=None):
    """Standard deviation along ``axis``, ignoring NaN and Inf (normalised by N).

    沿 ``axis`` 维求标准差，忽略 NaN 和 Inf（按 N 归一化）。
    """
    x = np.asarray(x, dtype=float)
    if axis is None:
        axis = first_non_singleton_axis(x)
    mean = smartmean(x, axis=axis)
    # Broadcast the mean back over the reduced axis.
    # 将均值广播回被消减的维度。
    shape = list(x.shape)
    shape.pop(axis)
    xc = x - np.asarray(mean).reshape(shape)
    # Normalize by N.
    # 按 N 归一化。
    # The N-1 variant is left commented out in MATLAB:
    # y=sqrt(smartsum(conj(xc).*xc,dim)/(smartsum(abs(sign(xc)), dim)-1));
    #   % normalize by N-1
    #   % 按 N-1 归一化
    return np.sqrt(smartmean(np.conj(xc) * xc, axis=axis))
