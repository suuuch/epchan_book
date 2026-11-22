"""Port of the MATLAB ``rows.m``: number of rows of a matrix.

PURPOSE: return rows in a matrix x
-----------------------------------------
USAGE: r = rows(x)
where: x = input matrix
-----------------------------------------
RETURNS: r = # of rows in x
-----------------------------------------
用途：返回矩阵 x 的行数
用法：r = rows(x)
其中：x = 输入矩阵
返回：r = x 的行数
"""

import numpy as np


def rows(x):
    """Return the number of rows of ``x``.

    返回 ``x`` 的行数。
    """
    return np.shape(x)[0]
