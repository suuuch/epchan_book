"""Port of the MATLAB ``tdis_inv.m`` written by Anders Holtsberg.

PURPOSE: returns the inverse (quantile) at x of the t(n) distribution.
USAGE: x = tdis_inv(p, n)
       where: p = a vector of probabilities
              n = a scalar dof parameter
RETURNS: a vector of tinv at each element of x of the t(n) distribution.
SEE ALSO: tdis_cdf, tdis_rnd, tdis_pdf, tdis_prb
用途: 返回 t(n) 分布在 x 处的反函数（分位数）
用法: x = tdis_inv(p, n)
      其中: p = 概率向量
             n = 标量自由度参数
返回: t(n) 分布在 x 各元素处的 tinv 值向量
参见: tdis_cdf, tdis_rnd, tdis_pdf, tdis_prb

Anders Holtsberg, 18-11-93
Copyright (c) Anders Holtsberg
版权所有 (c) Anders Holtsberg

Inverse of the cumulative distribution function (quantile) of Student's t
distribution with ``a`` degrees of freedom.
Student t 分布（自由度为 ``a``）累积分布函数（分位数）的反函数。
"""

import numpy as np

from .beta_inv import beta_inv


def tdis_inv(p, a):
    """Return the t quantile(s) for the probabilities ``p`` and ``a`` degrees of
    freedom.

    返回概率为 ``p``、自由度为 ``a`` 的 t 分布分位数。
    """
    p = np.asarray(p, dtype=float)
    s = p < 0.5
    p = p + (1.0 - 2.0 * p) * s
    p = 1.0 - 2.0 * (1.0 - p)
    x = beta_inv(p, 0.5, a / 2.0)
    x = x * a / (1.0 - x)
    x = (1.0 - 2.0 * s) * np.sqrt(x)
    return x
