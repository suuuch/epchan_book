"""Port of the MATLAB ``fwdshift.m`` written by Ernest Chan.

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com
编写者：
作者：Ernest Chan
著有"Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"一书

``fwdshift`` shifts a matrix *backward* in time: the first ``day`` rows are
dropped and ``day`` ``NaN`` rows are appended at the bottom.
``fwdshift`` 将矩阵沿时间轴向后移动：最前面的 ``day`` 行被丢弃，
并在底部追加 ``day`` 行 ``NaN``。
"""

import numpy as np

from .assert_ import assert_


def fwdshift(day, x):
    """Return ``x`` shifted backward by ``day`` rows (last rows are ``NaN``).

    返回沿时间轴向后平移 ``day`` 行后的 ``x``（最后几行为 ``NaN``）。
    """
    x = np.asarray(x)
    day = int(day)
    # assert(day >= 0)
    # 断言 day 大于等于 0
    assert_(day >= 0)
    pad = np.full((day,) + x.shape[1:], np.nan, dtype=float)
    body = x[day:]
    if x.ndim == 1:
        return np.concatenate([body, np.full(day, np.nan)])
    return np.vstack([body, pad])
