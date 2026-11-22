"""Port of the MATLAB ``rztcrit.m`` written by James P. LeSage.

Critical values for the ``Zt`` statistic used by :func:`epchan.cadf`.
返回 :func:`epchan.cadf` 中 Zt 统计量所用的临界值。

PURPOSE: return critical values for the Zt statistic used in cadf()
---------------------------------------------------------
USAGE:   crit = rztcrit(nobs,p);
where:   nobs = # of observations
            k = # of variables in x-matrix from cadf()
            p = order of time polynomial in the null-hypothesis
                p = -1, no deterministic part
                p =  0, for constant term
                p =  1, for constant plus time-trend
                p >  1, for higher order polynomial
         (the Python signature is rztcrit(nobs, k, p))
---------------------------------------------------------
NOTE: only works for p < 5
      Computed using 10000 iterations.
---------------------------------------------------------
RETURNS: crit = a (6 x 1) vector of critical values
                [1% 5% 10% 90% 95% 99%] quintiles
---------------------------------------------------------
References: Said and Dickey (1984) 'Testing for Unit Roots in
Autoregressive Moving Average Models of Unknown Order',
Biometrika, Volume 71, pp. 599-607.
用途: 返回 cadf() 中 Zt 统计量的临界值
用法: crit = rztcrit(nobs,p);
其中: nobs = 观测值个数
      k = cadf() 中 x 矩阵的变量个数
      p = 零假设中时间多项式的阶数
      p = -1, 无确定性部分
      p = 0, 用于常数项
      p = 1, 用于常数项加时间趋势
      p > 1, 用于更高阶多项式
      （Python 的函数签名为 rztcrit(nobs, k, p)）
注意: 仅适用于 p < 5
      使用 10000 次迭代计算得到。
返回: crit = 临界值向量 (6 x 1)
      [1% 5% 10% 90% 95% 99%] 分位数
参考文献: Said and Dickey (1984)《Testing for Unit Roots in
Autoregressive Moving Average Models of Unknown Order》
Biometrika, 第 71 卷, 第 599-607 页.

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jlesage@spatia-econometrics.com
编写者:
"""

from ._rztcrit_tables import TABLES


def rztcrit(nobs, k, p):
    """Return the 6 critical values used by the augmented Dickey-Fuller test.

    ``nobs`` is the number of observations, ``k`` the number of variables of
    the ``x`` matrix and ``p`` the order of the time polynomial of the null
    hypothesis (``-1`` none, ``0`` constant, ``1`` constant plus trend).

    The returned vector holds the ``[1% 5% 10% 90% 95% 99%]`` quintiles.

    Unlike the MATLAB original, which silently indexes past the end of the
    table when ``k`` or ``p`` is out of range, a ``ValueError`` is raised for
    combinations that are not tabulated.

    ``nobs`` 是观测值个数，``k`` 是 ``x`` 矩阵中变量的个数，``p`` 是零假设
    中时间多项式的阶数（``-1`` 表示没有确定性部分，``0`` 表示常数项，
    ``1`` 表示常数项加时间趋势）。

    返回的向量包含 ``[1% 5% 10% 90% 95% 99%]`` 分位数。

    与 MATLAB 原始版本不同：当 ``k`` 或 ``p`` 超出表格范围时，原始版本会
    静默地索引到表格之外，而这里对没有制表的数据组合抛出 ``ValueError``。
    """
    nobs = int(nobs)
    k = int(k)
    p = int(p)

    table = None
    for _name, (low, high), values in TABLES:
        if nobs >= low and (high is None or nobs <= high):
            table = values
            break
    if table is None:
        raise ValueError("no critical values available for nobs=%d" % nobs)

    # The MATLAB code computes the row index as n = (k-1)*7 + p + 2.
    # MATLAB 代码用 n = (k-1)*7 + p + 2 计算行索引。
    n = (k - 1) * 7 + p + 2
    if n < 1 or n > table.shape[0]:
        raise ValueError(
            "critical values are not tabulated for k=%d and p=%d" % (k, p))
    return table[n - 1, :].reshape(6, 1)
