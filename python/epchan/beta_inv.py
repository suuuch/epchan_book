"""Port of the MATLAB ``beta_inv.m`` written by Anders Holtsberg.

PURPOSE: inverse of the cdf (quantile) of the beta(a,b) distribution
--------------------------------------------------------------
USAGE: x = beta_inv(p,a,b)
where:   p = vector of probabilities
         a = beta distribution parameter, a = scalar
         b = beta distribution parameter  b = scalar
NOTE: mean [beta(a,b)] = a/(a+b), variance = ab/((a+b)*(a+b)*(a+b+1))
--------------------------------------------------------------
RETURNS: x at each element of p for the beta(a,b) distribution
--------------------------------------------------------------
SEE ALSO: beta_d, beta_pdf, beta_inv, beta_rnd
--------------------------------------------------------------
用途: beta(a,b) 分布的 cdf (分位数) 的逆函数
用法: x = beta_inv(p,a,b)
其中:   p = 概率向量
        a = beta 分布参数, a = 标量
        b = beta 分布参数  b = 标量
注意: mean[beta(a,b)] = a/(a+b), 方差 = ab/((a+b)*(a+b)*(a+b+1))
返回: beta(a,b) 分布下 p 各元素对应的 x
参见: beta_d, beta_pdf, beta_inv, beta_rnd

      Anders Holtsberg, 18-11-93
      Copyright (c) Anders Holtsberg
documentation modified by LeSage to
match the format of the econometrics toolbox
作者: Anders Holtsberg, 18-11-93
版权所有 (c) Anders Holtsberg
文档由 LeSage 修改以匹配计量经济学工具箱的格式

Inverse of the cumulative distribution function (quantile) of the beta
distribution, computed with the very same Newton iteration as the original.
求 beta 分布累积分布函数（分位数）的逆函数，
使用与原版完全相同的牛顿迭代法求解。
"""

import numpy as np
from scipy.stats import beta as beta_dist

from .beta_pdf import beta_pdf

_EPS = np.finfo(float).eps


def beta_inv(p, a, b):
    """Quantile of the ``beta(a, b)`` distribution for each probability in ``p``.

    返回 ``p`` 中各概率所对应的 ``beta(a, b)`` 分布分位数。
    """
    p = np.asarray(p, dtype=float)
    if np.any(np.asarray(a) <= 0) or np.any(np.asarray(b) <= 0):
        raise ValueError("beta_inv parameter a or b is nonpositive")
    if np.any(np.abs(2.0 * p - 1.0) > 1.0):
        raise ValueError("beta_inv: A probability should be 0<=p<=1")

    x = np.full(p.shape, a / (a + b), dtype=float)
    dx = np.ones_like(x)
    # The original MATLAB code has no iteration limit; a guard is added here so
    # that a pathological input cannot hang the program.
    # 原 MATLAB 代码没有迭代次数上限；这里加了一个保护，
    # 以免病态输入导致程序卡死。
    for _ in range(200):
        if not np.any(np.abs(dx) > 256.0 * _EPS * np.maximum(x, 1.0)):
            break
        x_eval = np.clip(x, np.finfo(float).tiny, 1.0 - np.finfo(float).eps)
        dx = (beta_dist.cdf(x_eval, a, b) - p) / beta_pdf(x_eval, a, b)
        x = x - dx
        # The original line is 'x = x + (dx - x)/2 .* (x<0)'.
        # 原代码为 'x = x + (dx - x)/2 .* (x<0)'。
        x = x + (dx - x) / 2.0 * (x < 0)
    return x
