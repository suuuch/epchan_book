"""Port of the MATLAB ``beta_pdf.m`` written by Anders Holtsberg.

PURPOSE: pdf of the beta(a,b) distribution
--------------------------------------------------------------
USAGE: pdf = beta_pdf(x,a,b)
where:   x = vector of components
         a = beta distribution parameter, a = scalar
         b = beta distribution parameter  b = scalar
NOTE: mean[(beta(a,b)] = a/(a+b), variance = ab/((a+b)*(a+b)*(a+b+1))
--------------------------------------------------------------
RETURNS: pdf at each element of x of the beta(a,b) distribution
--------------------------------------------------------------
SEE ALSO: beta_d, beta_pdf, beta_inv, beta_rnd
--------------------------------------------------------------
用途: beta(a,b) 分布的概率密度函数(pdf)
用法: pdf = beta_pdf(x,a,b)
其中:   x = 分量向量
        a = beta 分布参数, a = 标量
        b = beta 分布参数  b = 标量
注意: mean[beta(a,b)] = a/(a+b), 方差 = ab/((a+b)*(a+b)*(a+b+1))
返回: beta(a,b) 分布下 x 各元素处的 pdf
参见: beta_d, beta_pdf, beta_inv, beta_rnd

      Anders Holtsberg, 18-11-93
      Copyright (c) Anders Holtsberg
documentation modified by LeSage to
match the format of the econometrics toolbox
作者: Anders Holtsberg, 18-11-93
版权所有 (c) Anders Holtsberg
文档由 LeSage 修改以匹配计量经济学工具箱的格式

Probability density function of the beta distribution.
beta 分布的概率密度函数。
"""

import numpy as np
from scipy.special import beta as beta_


def beta_pdf(x, a, b):
    """Density of the ``beta(a, b)`` distribution evaluated at ``x``.

    在 ``x`` 处求 ``beta(a, b)`` 分布的概率密度。
    """
    x = np.asarray(x, dtype=float)
    if np.any(np.asarray(a) <= 0) or np.any(np.asarray(b) <= 0):
        raise ValueError("Parameter a or b is nonpositive")

    pdf = np.zeros_like(x, dtype=float)
    # MATLAB: I = find((x<0)|(x>1)); ... pdf(I) = 0*I;
    # MATLAB 中先找出落在支持集 [0,1] 之外的元素，再把其 pdf 置为 0。
    inside = np.isfinite(x) & (x >= 0) & (x <= 1)
    xi = x[inside]
    with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
        pdf[inside] = xi ** (a - 1.0) * (1.0 - xi) ** (b - 1.0) / beta_(a, b)
    return pdf
