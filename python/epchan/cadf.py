"""Port of the MATLAB ``cadf.m`` written by James P. LeSage.

PURPOSE: compute augmented Dickey-Fuller statistic for residuals
         from a cointegrating regression, allowing for deterministic
         polynomial trends
用途: 计算协整回归残差的增广 Dickey-Fuller 统计量
允许存在确定性多项式趋势

USAGE: results = cadf(y,x,p,nlag)
where: y = dependent variable time-series vector
       x = explanatory variables matrix
            p = order of time polynomial in the null-hypothesis
                p = -1, no deterministic part
                p =  0, for constant term
                p =  1, for constant plus time-trend
                p >  1, for higher order polynomial
    nlag = # of lagged changes of the residuals to include in regression
用法: results = cadf(y,x,p,nlag)
其中: y = 被解释变量时间序列向量
      x = 解释变量矩阵
           p = 零假设中时间多项式的阶数
               p = -1, 无确定性部分
               p =  0, 含常数项
               p =  1, 含常数项和时间趋势
               p >  1, 含更高阶多项式
      nlag = 回归中纳入的残差滞后差分个数

RETURNS: results structure
         results.meth  = 'cadf'
         results.alpha = autoregressive parameter estimate
         results.adf   = ADF t-statistic
         results.crit  =  (6 x 1) vector of critical values
                       [1% 5% 10% 90% 95% 99%] quintiles
         results.nvar  = cols(x)
         results.nlag  = nlag
返回: results 结构体
其中: results.meth  = 'cadf'
其中: results.alpha = 自回归参数估计值
其中: results.adf   = ADF t 统计量
其中: results.crit  =  (6 x 1) 临界值向量, 对应 [1% 5% 10% 90% 95% 99%] 分位数
其中: results.nvar  = cols(x)
其中: results.nlag  = nlag

SEE ALSO: prt_coint()
参见: prt_coint()

References: Said and Dickey (1984) 'Testing for Unit Roots in
Autoregressive Moving Average Models of Unknown Order',
Biometrika, Volume 71, pp. 599-607.
参考文献: Said and Dickey (1984) 'Testing for Unit Roots in Autoregressive
Moving Average Models of Unknown Order',
Biometrika, 第 71 卷, 第 599-607 页。

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jlesage@spatial-econometrics.com
编写者:

Modeled after a similar Gauss routine by
Sam Ouliaris, in a package called COINT
仿照以下作者的类似 Gauss 例程:
Sam Ouliaris, 在名为 COINT 的程序包中
"""

from dataclasses import dataclass

import numpy as np

from .cols import cols
from .lag import lag
from .matlab_compat import detrend, left_divide
from .rows import rows
from .rztcrit import rztcrit
from .tdiff import tdiff
from .trimr import trimr


@dataclass
class CadfResults:
    """The results structure returned by :func:`cadf` (same fields as MATLAB).

    返回的 results 结构体, 字段与 MATLAB 版本完全一致。
    """

    meth: str = "cadf"
    alpha: float = np.nan
    adf: float = np.nan
    crit: np.ndarray = None
    nvar: int = 0
    nlag: int = 0


def cadf(y, x, p, l):
    """Augmented Dickey-Fuller test on the residuals of ``y`` regressed on ``x``.

    ``y`` is the dependent variable (a vector), ``x`` the matrix of
    explanatory variables, ``p`` the order of the time polynomial of the null
    hypothesis and ``l`` the number of lagged differences of the residuals
    (MATLAB calls this one ``nlag``).
    对 ``y`` 关于 ``x`` 回归所得残差进行增广 Dickey-Fuller 检验。

    ``y`` 是被解释变量 (向量), ``x`` 是解释变量矩阵, ``p`` 是零假设中时间
    多项式的阶数, ``l`` 是残差滞后差分的个数 (MATLAB 中称为 ``nlag``)。
    """
    # error checking
    # 错误检查
    if p < -1:
        raise ValueError("p cannot be < -1 in cadf")

    y = np.asarray(y, dtype=float).ravel()
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)

    nobs = rows(x)
    if nobs - (2 * l) + 1 < 1:
        raise ValueError("nlags is too large in cadf; negative degrees of freedom")

    y = detrend(y, p)
    x = detrend(x, p)

    b = np.linalg.inv(x.T @ x) @ (x.T @ y)
    r = y - x @ b

    dep = tdiff(r, 1)
    dep = trimr(dep, 1, 0)

    z = trimr(lag(r, 1), 1, 0)
    for k in range(1, l + 1):
        z = np.hstack([z, lag(dep, k)])
    z = trimr(z, l, 0)
    dep = trimr(dep, l, 0)

    beta = left_divide(detrend(z, 0), detrend(dep, 0))
    # res     = dep - z*beta ;
    # 已注释掉的语句: res     = dep - z*beta ;
    # BUG fix suggested by Nick Firoozye
    # BUG 修复建议由以下人员提出: Nick Firoozye
    # Sanford C. Bernstein, Inc
    # 767 Fifth Avenue, #21-49
    # New York, NY 10153
    res = detrend(dep, 0) - detrend(z, 0) @ beta

    so = float(res.ravel() @ res.ravel()) / (rows(dep) - cols(z))
    var_cov = so * np.linalg.inv(z.T @ z)

    results = CadfResults()
    results.alpha = beta[0, 0]
    results.adf = beta[0, 0] / np.sqrt(var_cov[0, 0])
    results.crit = rztcrit(nobs, cols(x), p)
    results.nlag = l
    results.nvar = cols(x)
    return results
