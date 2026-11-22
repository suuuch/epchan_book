"""Port of the MATLAB ``smartmean.m``.

PURPOSE: SMARTMEAN -- average or mean value ignoring NaN.
         Same as MEAN except that it returns the mean of the finite elements
         instead of propagating NaN and Inf.
         Returns NaN if there are no finite elements.

         For vectors, MEAN(X) is the mean value of the elements in X.  For
         matrices, MEAN(X) is a row vector containing the mean value of
         each column.  For N-D arrays, MEAN(X) is the mean value of the
         elements along the first non-singleton dimension of X.

         MEAN(X,DIM) takes the mean along the dimension DIM of X.

         Example: If X = [0 1 2
                           3 4 5]

         then mean(X,1) is [1.5 2.5 3.5] and mean(X,2) is [1
                                                               4]

USAGE: smartmean(x)
       smartmean(x, dim)
       where: x = input array
              dim = dimension along which the mean is taken

RETURNS: the average of the finite elements along ``dim``.

SEE ALSO: MEDIAN, STD, MIN, MAX, COV.

用途: SMARTMEAN -- 忽略 NaN 的平均值或均值。
      与 MEAN 相同，但它返回有限元素的均值，而不是传播 NaN 和 Inf。
      若不存在有限元素则返回 NaN。

      对向量，MEAN(X) 是 X 中各元素的均值。对矩阵，MEAN(X) 是包含各列
      均值的行向量。对于 N 维数组，MEAN(X) 是沿 X 第一个非单例维度的
      元素均值。

      MEAN(X,DIM) 沿 X 的 DIM 维度求均值。

      例如: 若 X = [0 1 2
                     3 4 5]

      则 mean(X,1) 为 [1.5 2.5 3.5]，mean(X,2) 为 [1
                                                     4]

用法: smartmean(x)
      smartmean(x, dim)
      其中: x = 输入数组
             dim = 求均值的维度

返回: 沿 ``dim`` 维的有限元素均值。

参见: MEDIAN, STD, MIN, MAX, COV.

Copyright (c) 1984-98 by The MathWorks, Inc.
$Revision: 5.13 $  $Date: 1997/11/21 23:23:55 $
版权所有 (c) 1984-98 The MathWorks, Inc.
修订: $Revision: 5.13 $  日期: $Date: 1997/11/21 23:23:55 $
"""

import numpy as np

from .matlab_compat import first_non_singleton_axis


def smartmean(x, axis=None):
    """Average of the finite elements of ``x`` along ``axis``.

    Columns (or slices) that contain no finite value at all become ``NaN``.
    ``axis`` is a 0-based numpy axis; when omitted the first non singleton
    axis is used, exactly like MATLAB.

    沿 ``axis`` 维求 ``x`` 中有限元素的平均值。

    完全不含有限值的列（或切片）会变成 ``NaN``。
    ``axis`` 是从 0 开始的 numpy 轴；省略时使用第一个非单例轴，
    与 MATLAB 完全一致。
    """
    x = np.asarray(x, dtype=float)
    if axis is None:
        # Determine which dimension SUM will use.
        # 确定 SUM 将使用的维度。
        axis = first_non_singleton_axis(x)
    has_data = np.isfinite(x)
    xs = np.where(has_data, x, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        y = xs.sum(axis=axis) / has_data.sum(axis=axis)
    all_bad = np.all(~has_data, axis=axis)
    return np.where(all_bad, np.nan, y)
