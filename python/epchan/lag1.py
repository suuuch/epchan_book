"""Port of the MATLAB ``lag1.m`` written by Ernest Chan.

``lag1`` shifts a matrix down by one row and pads the first row with ``NaN``
(or with ``''`` for character arrays).
``lag1`` 将矩阵整体下移一行, 并用 ``NaN`` (字符数组则用 ``''``) 填充第一行。

USAGE: y=lag(x)
用法：y=lag(x)

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com
编写者:
作者 Ernest Chan
著有《Quantitative Trading:
How to Start Your Own Algorithmic Trading Business?》一书。
"""

import numpy as np


def lag1(x):
    """Return ``x`` lagged by one observation (first row filled with ``NaN``).

    返回滞后一个观测值的 ``x`` (第一行用 ``NaN`` 填充)。
    """
    x = np.asarray(x)
    if x.ndim == 1:
        if x.dtype.kind in "US":
            # populate the first entry with ''
            # 将第一个元素填充为 ''
            empty = np.array([""], dtype=x.dtype)
        else:
            # populate the first entry with NaN
            # 将第一个元素填充为 NaN
            empty = np.array([np.nan])
        return np.concatenate([empty, x[:-1]])
    if x.dtype.kind in "US":
        # populate the first entry with ''
        # 将第一个元素填充为 ''
        empty = np.full((1,) + x.shape[1:], "", dtype=x.dtype)
    else:
        # y=[NaN(1,size(x,2));x(1:end-1, :)]; % populate the first entry with NaN
        # 将第一个元素填充为 NaN
        # populate the first entry with NaN
        # 将第一个元素填充为 NaN
        empty = np.full((1,) + x.shape[1:], np.nan, dtype=float)
    return np.vstack([empty, x[:-1]])
