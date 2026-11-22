"""Port of the MATLAB ``cols.m``: number of columns of a matrix.

PURPOSE: return columns in a matrix x
-----------------------------------------
USAGE: c = cols(x)
where: x = input matrix
-----------------------------------------
RETURNS: c = # of columns in x
-----------------------------------------
用途：返回矩阵 x 的列数
用法：c = cols(x)
其中：x = 输入矩阵
返回：c = x 的列数
"""

import numpy as np


def cols(x):
    """Return the number of columns of ``x``.

    A one dimensional array is treated as a column vector, so ``cols`` returns
    ``1`` for it, just like MATLAB does for ``n x 1`` vectors.
    一维数组被视为列向量，因此 ``cols`` 对其返回 ``1``，
    与 MATLAB 对 ``n x 1`` 向量的处理方式相同。
    """
    shape = np.shape(x)
    if len(shape) < 2:
        return 1
    return shape[1]
