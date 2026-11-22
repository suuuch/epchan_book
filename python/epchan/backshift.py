"""Port of the MATLAB ``backshift.m`` written by Ernest Chan.

y = backshift(day, x)

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com
用法: y = backshift(day, x)
编写者：
作者：Ernest Chan
著有"Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"一书

``backshift`` shifts a matrix *forward* in time: the first ``day`` rows become
``NaN`` and the last ``day`` rows are dropped, so the number of rows is
unchanged.
``backshift`` 将矩阵沿时间轴向前移动：最前面的 ``day`` 行变为 ``NaN``，
最后的 ``day`` 行被丢弃，因此行数保持不变。
"""

import numpy as np


def backshift(day, x):
    """Return ``x`` shifted forward by ``day`` rows (first rows are ``NaN``).

    返回沿时间轴向前平移 ``day`` 行后的 ``x``（最前面的几行为 ``NaN``）。
    """
    x = np.asarray(x)
    day = int(day)
    # assert(day >= 0)
    # 断言 day 大于等于 0
    if day < 0:
        raise ValueError("day = %d < 0, error!" % day)
    # y = [NaN(day, size(x, 2), size(x, 3)); x(1:end-day, :, :)]
    # 在前面补上 day 行 NaN
    n = x.shape[0]
    body = x[:max(n - day, 0)]
    if x.ndim == 1:
        return np.concatenate([np.full(day, np.nan), body])
    pad = np.full((day,) + x.shape[1:], np.nan, dtype=float)
    return np.vstack([pad, body])
