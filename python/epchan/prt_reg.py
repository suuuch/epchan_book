"""Print the output of an ordinary least squares regression.

The MATLAB original relies on ``prt_reg.m``, a file that is *not* part of this
repository, but ``prt.m`` calls it for every regression result.  This module
provides the missing counterpart so that :func:`epchan.prt` works for the
``ols`` results as well.
MATLAB 原始版本依赖 ``prt_reg.m``，但该文件并不在本仓库中，而 ``prt.m``
对每一个回归结果都会调用它。本模块提供了缺失的对应实现，使得
:func:`epchan.prt` 同样可以处理 ``ols`` 的结果。

PURPOSE: Prints the output of a regression results structure produced by
         ``ols`` (and by the other regression methods dispatched by
         ``prt.m``).
---------------------------------------------------
USAGE: prt_reg(results,vnames,fid)
Where: results = a results structure returned by a regression function
       vnames  = an optional vector of variable names
                 (defaults to generic names x1, x2, ...)
       fid     = file-id for printing results to a file
                 (defaults to the MATLAB command window)
---------------------------------------------------
              e.g. vnames = ['y    ',
                             'x1   ',  NOTE: fixed width
                             'x2   ',        like all MATLAB
                             'cterm'];       strings
              e.g. fid = fopen('ols.out','wr');
--------------------------------------------------
RETURNS:
       nothing, just prints the regression results
--------------------------------------------------
SEE ALSO: prt(results), plt(results)
---------------------------------------------------
用途: 打印回归结果结构（由 ``ols`` 以及 ``prt.m`` 分派的其它回归方法
      产生）的输出结果。
---------------------------------------------------
用法: prt_reg(results,vnames,fid)
其中: results = 回归函数返回的结果结构
      vnames  = 可选的变量名向量
                （默认使用 x1、x2 等通用名称）
      fid     = 用于将结果打印到文件的文件标识符
                （默认为 MATLAB 命令窗口）
---------------------------------------------------
      例如 vnames = ['y    ',
                     'x1   ',  注意: 固定宽度
                     'x2   ',        与所有 MATLAB
                     'cterm'];       字符串相同
      例如 fid = fopen('ols.out','wr');
--------------------------------------------------
返回:
无返回值, 仅打印回归结果
--------------------------------------------------
参见: prt(results), plt(results)

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jlesage@spatial-econometrics.com
编写者:
"""

import sys

import numpy as np


def prt_reg(results, vnames=None, fid=None):
    """Print the results of an :func:`epchan.ols` regression.

    The table lists, for every explanatory variable, the coefficient, its
    standard error, the t statistic, the two-sided p-value and the 95%
    confidence interval; the R-squared, the adjusted R-squared, the
    Durbin-Watson statistic and the number of observations follow below.

    表格按解释变量逐行列出回归系数、标准误、t 统计量、双侧 p 值以及
    95% 置信区间；表格下方依次给出 R 平方、调整后的 R 平方、
    Durbin-Watson 统计量和观测值个数。
    """
    if fid is None:
        fid = sys.stdout

    beta = np.asarray(results.beta).ravel()
    tstat = np.asarray(results.tstat).ravel()
    bstd = np.asarray(results.bstd).ravel()
    bint = np.asarray(results.bint).reshape(len(beta), 2)

    # no variable names supplied, make some up
    # 未提供变量名，自行构造
    if vnames is None or len(vnames) == 0:
        names = ["x%d" % (i + 1) for i in range(len(beta))]
    else:
        names = [str(v) for v in vnames]

    nobs = results.nobs
    nvar = results.nvar

    fid.write("\n")
    fid.write("%-14s %12s %12s %10s %8s %12s %12s\n"
              % ("Variable", "Coefficient", "Std Error", "t-stat", "Prob(>t)",
                 "95% Lower", "95% Upper"))
    fid.write("%s\n" % ("-" * 80))
    for i, name in enumerate(names):
        prob = _t_sf(abs(tstat[i]), nobs - nvar)
        fid.write("%-14s %12.6f %12.6f %10.4f %8.4f %12.6f %12.6f\n"
                  % (name, beta[i], bstd[i], tstat[i], prob, bint[i, 0], bint[i, 1]))
    fid.write("\n")
    fid.write("R-squared          %12.6f\n" % results.rsqr)
    fid.write("R-bar-squared      %12.6f\n" % results.rbar)
    fid.write("Durbin-Watson stat %12.6f\n" % results.dw)
    fid.write("Observations       %12d\n" % nobs)


def _t_sf(t, dof):
    """Two sided p-value of a t statistic.

    t 统计量的双侧 p 值。
    """
    try:
        from scipy.stats import t as t_dist
    except ImportError:  # pragma: no cover - scipy is a hard dependency
        return float("nan")
    if dof <= 0:
        return float("nan")
    return float(2.0 * t_dist.sf(abs(t), dof))
