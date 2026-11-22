"""Port of the MATLAB ``ols.m`` written by James P. LeSage (and Barry Dillon).

Ordinary least squares regression.
普通最小二乘回归。

PURPOSE: least-squares regression
---------------------------------------------------
USAGE: results = ols(y,x)
where: y = dependent variable vector    (nobs x 1)
       x = independent variables matrix (nobs x nvar)
---------------------------------------------------
RETURNS: a structure
       results.meth  = 'ols'
       results.beta  = bhat     (nvar x 1)
       results.tstat = t-stats  (nvar x 1)
       results.bstd  = std deviations for bhat (nvar x 1)
       results.yhat  = yhat     (nobs x 1)
       results.resid = residuals (nobs x 1)
       results.sige  = e'*e/(n-k)   scalar
       results.rsqr  = rsquared     scalar
       results.rbar  = rbar-squared scalar
       results.dw    = Durbin-Watson Statistic
       results.nobs  = nobs
       results.nvar  = nvars
       results.y     = y data vector (nobs x 1)
       results.bint  = (nvar x2 ) vector with 95% confidence intervals on beta
---------------------------------------------------
SEE ALSO: prt(results), plt(results)
---------------------------------------------------
用途: 最小二乘回归
用法: results = ols(y,x)
其中: y = 因变量向量    (nobs x 1)
      x = 自变量矩阵 (nobs x nvar)
返回: 一个结构体
      results.meth  = 'ols'，表示估计方法
      results.beta  = bhat     (nvar x 1)，回归系数
      results.tstat = t-stats  (nvar x 1)，t 统计量
      results.bstd  = bhat 的标准差 (nvar x 1)
      results.yhat  = yhat     (nobs x 1)，拟合值
      results.resid = residuals (nobs x 1)，残差
      results.sige  = e'*e/(n-k)   标量，残差方差
      results.rsqr  = rsquared     标量，R 平方
      results.rbar  = rbar-squared 标量，调整后的 R 平方
      results.dw    = Durbin-Watson 统计量
      results.nobs  = nobs，观测值个数
      results.nvar  = nvars，自变量个数
      results.y     = y 数据向量 (nobs x 1)
      results.bint  = (nvar x 2) 向量，包含 beta 的 95% 置信区间
参见: prt(results), plt(results)

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jlesage@spatial-econometrics.com

Barry Dillon (CICG Equity)
added the 95% confidence intervals on bhat
编写者:
Barry Dillon (CICG Equity)：增加了 bhat 的 95% 置信区间
"""

from dataclasses import dataclass

import numpy as np

from .tdis_inv import tdis_inv


@dataclass
class OlsResults:
    """The results structure returned by :func:`ols` (same fields as MATLAB).

    由 :func:`ols` 返回的结果结构体（字段与 MATLAB 相同）。
    """

    meth: str = "ols"
    y: np.ndarray = None
    nobs: int = 0
    nvar: int = 0
    beta: np.ndarray = None
    yhat: np.ndarray = None
    resid: np.ndarray = None
    sige: float = np.nan
    bstd: np.ndarray = None
    tstat: np.ndarray = None
    bint: np.ndarray = None
    rsqr: float = np.nan
    rbar: float = np.nan
    dw: float = np.nan


def ols(y, x):
    """Least squares regression of ``y`` on ``x``.

    ``y`` is a vector of ``nobs`` observations and ``x`` an ``(nobs x nvar)``
    matrix of explanatory variables.

    ``y`` 是包含 ``nobs`` 个观测值的向量，``x`` 是 ``(nobs x nvar)``
    的解释变量矩阵。
    """
    y = np.asarray(y, dtype=float).ravel().reshape(-1, 1)
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)

    nobs, nvar = x.shape
    if nobs != y.size:
        raise ValueError("x and y must have same # obs in ols")

    results = OlsResults(y=y, nobs=nobs, nvar=nvar)

    if nobs < 10000:
        # QR decomposition, like the original code.
        # 与原始代码相同，使用 QR 分解。
        _q, r = np.linalg.qr(x, mode="reduced")
        xpxi = np.linalg.inv(r.T @ r)
    else:
        # use Cholesky for very large problems
        # 对非常大的问题使用 Cholesky 分解
        xpxi = np.linalg.inv(x.T @ x)

    results.beta = xpxi @ (x.T @ y)
    results.yhat = x @ results.beta
    results.resid = y - results.yhat
    sigu = float(results.resid.ravel() @ results.resid.ravel())
    results.sige = sigu / (nobs - nvar)
    # ``tmp`` is a column vector, like MATLAB's ``sige*diag(xpxi)``.
    # ``tmp`` 是列向量，与 MATLAB 的 ``sige*diag(xpxi)`` 一致。
    tmp = (results.sige * np.diag(xpxi)).reshape(-1, 1)
    sigb = np.sqrt(tmp)
    results.bstd = sigb
    tcrit = -tdis_inv(0.025, nobs)
    results.bint = np.column_stack([results.beta - tcrit * sigb,
                                    results.beta + tcrit * sigb])
    results.tstat = results.beta / np.sqrt(tmp)
    ym = y - y.mean()
    rsqr1 = sigu
    rsqr2 = float(ym.ravel() @ ym.ravel())
    # r-squared
    # R 平方
    results.rsqr = 1.0 - rsqr1 / rsqr2
    rsqr1 = rsqr1 / (nobs - nvar)
    rsqr2 = rsqr2 / (nobs - 1.0)
    if rsqr2 != 0:
        # rbar-squared
        # 调整后的 R 平方
        results.rbar = 1.0 - (rsqr1 / rsqr2)
    else:
        results.rbar = results.rsqr
    ediff = results.resid[1:] - results.resid[:-1]
    # durbin-watson
    # Durbin-Watson 统计量
    results.dw = float(ediff.ravel() @ ediff.ravel()) / sigu
    return results
