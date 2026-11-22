"""Port of the MATLAB ``tdiff.m`` written by James P. LeSage.

PURPOSE: produce matrix differences
用途: 生成矩阵差分

USAGE: dmat = tdiff(x,k)
where:    x = input matrix (or vector) of length nobs
          k = lagged difference order
用法: dmat = tdiff(x,k)
其中: x = 长度为 nobs 的输入矩阵（或向量）
      k = 差分的滞后阶数

NOTE: uses trimr() and lag()
注意: 使用 trimr() 和 lag()

RETURNS: dmat = matrix or vector, differenced by k-periods
                e.g. x(t) - x(t-k), of length nobs,
                (first k observations are zero)
返回: dmat = 按 k 期差分后的矩阵或向量
      例如 x(t) - x(t-k)，长度为 nobs,
      (前 k 个观测值为零)

SEE ALSO: trimr() modeled after Gauss trimr function
参见: trimr()，仿照 Gauss 的 trimr 函数编写

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jpl@jpl.econ.utoledo.edu
编写者:

Produces ``x(t) - x(t-k)``; the first ``k`` observations are zero.
生成 ``x(t) - x(t-k)``；前 ``k`` 个观测值为零。
"""

import numpy as np


def tdiff(x, k):
    """Return the ``k``-period difference of ``x``.

    The shape of ``x`` is preserved: a vector stays a vector, a matrix stays a
    matrix, exactly like the MATLAB function.
    返回 ``x`` 的 ``k`` 期差分。

    ``x`` 的形状保持不变: 向量仍是向量, 矩阵仍是矩阵, 与 MATLAB 函数完全一致。
    """
    x = np.asarray(x, dtype=float)
    # error checking on inputs
    # 对输入进行错误检查
    if x.ndim > 2:
        raise ValueError("tdiff expects a vector or a matrix")
    if k == 0:
        return x.copy()

    # modified by Jushan Bai
    # 由 Jushan Bai 修改
    # NYU
    # 纽约大学 (NYU)
    # tmp = x - lag(x,1);
    # 先用一阶滞后差分 tmp = x - lag(x,1);
    # for ndiff = 2:k;
    # 对 ndiff = 2:k 进行循环;
    # tmp = tmp - lag(tmp,1);
    # 逐阶差分 tmp = tmp - lag(tmp,1);
    # end;
    # 结束;
    # dmat = tmp;
    # 结果为 dmat = tmp;
    dmat = np.zeros_like(x)
    dmat[k:] = x[k:] - x[:-k]
    return dmat
