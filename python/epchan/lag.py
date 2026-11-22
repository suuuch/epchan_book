"""Port of the MATLAB ``lag.m`` written by James P. LeSage.

``lag`` pads the top of the matrix with a constant (0 by default) and drops
the same number of rows at the bottom.  It is *not* the same as :func:`lag1`,
which pads with ``NaN``.
``lag`` 在矩阵顶部填充一个常数 (默认为 0), 并在底部丢弃同样数量的行。
它与 :func:`lag1` 不同, 后者用 ``NaN`` 填充。

PURPOSE: creates a matrix or vector of lagged values
用途: 创建滞后值的矩阵或向量

USAGE: z = lag(x,n,v)
where: x = input matrix or vector, (nobs x k)
       n = order of lag
       v = (optional) initial values (default=0)
e.g.
    z = lag(x) creates a matrix (or vector) of x, lagged 1 observations
    z = lag(x,n) creates a matrix (or vector) of x, lagged n observations
    z = lag(x,n,v) creates a matrix (or vector) of x, lagged n observations,
        with initial values taking a value v.
用法: z = lag(x,n,v)
其中: x = 输入矩阵或向量, (nobs x k)
      n = 滞后的阶数
      v = (可选) 初始值 (默认值=0)
例如:
    z = lag(x) 创建 x 滞后 1 个观测值的矩阵 (或向量)
    z = lag(x,n) 创建 x 滞后 n 个观测值的矩阵 (或向量)
    z = lag(x,n,v) 创建 x 滞后 n 个观测值的矩阵 (或向量), 初始值取 v。

RETURNS: z = matrix (or vector) of lags (nobs x k)
返回: z = 滞后值的矩阵 (或向量) (nobs x k)

NOTES: if n <= 0, z = [] is returned. While you may find this
       perverse, it is sometimes useful.
注意: 如果 n <= 0, 将返回 z = []。虽然你可能觉得这样做很荒谬, 但有时还是很有用的。

SEE ALSO: mlag()
参见: mlag()

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jpl@jpl.econ.utoledo.edu
编写者:
"""

import numpy as np

from .cols import cols


def lag(x, n=1, v=0.0):
    """Return ``x`` lagged by ``n`` observations, padded with ``v``.

    ``n <= 0`` returns an empty array, as in MATLAB.

    A one dimensional input gives a one dimensional result here, whereas
    MATLAB always returns a matrix (a Python 1-D array is closer to a MATLAB
    column vector in the rest of this package).
    返回滞后 ``n`` 个观测值、并以 ``v`` 填充开头的 ``x``。

    ``n <= 0`` 时返回空数组, 与 MATLAB 行为一致。

    这里一维输入会得到一维结果, 而 MATLAB 始终返回矩阵 (在本包的其余部分,
    Python 的一维数组更接近 MATLAB 的列向量)。
    """
    x = np.asarray(x)
    # MATLAB dispatches on nargin; n=1 and v=0 are the defaults here.
    # MATLAB 按 nargin 分支处理; 此处以 n=1、v=0 作为默认值。
    if n < 1:
        return np.empty((0,) + x.shape[1:], dtype=x.dtype)
    pad = np.full((n, cols(x)), v, dtype=float)
    if x.ndim == 1:
        pad = pad[:, 0]
        return np.concatenate([pad, x[:x.shape[0] - n]])
    return np.vstack([pad, x[:x.shape[0] - n]])
