"""Port of the MATLAB ``fillMissingData.m`` written by Ernest Chan.

[filledPrices] = fillMissingData(prices)
fill data in a 2-dim array with NaN's with the previous value.

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com
用法：[filledPrices]=fillMissingData(prices)，用前一个值填补
二维数组中的 NaN 缺失值。
编写者：
作者：Ernest Chan
著有"Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"一书
"""

import numpy as np


def fill_missing_data(prices):
    """Fill the NaN/Inf entries of a 2-D array with the previous value.

    The first row is left untouched, exactly as in the MATLAB code.
    用前一个值填补二维数组中的 NaN/Inf 缺失值。
    第一行保持原样，与 MATLAB 代码完全一致。
    """
    filled = np.array(prices, dtype=float, copy=True)
    for t in range(1, filled.shape[0]):
        miss_data = ~np.isfinite(filled[t, :])
        filled[t, miss_data] = filled[t - 1, miss_data]
    return filled
