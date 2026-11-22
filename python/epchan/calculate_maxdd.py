"""Port of the MATLAB ``calculateMaxDD.m`` written by Ernest Chan.

Maximum drawdown and maximum drawdown duration of a series of *cumulative
compounded* returns.
一组 *累计 COMPOUNDED* 收益率的最大回撤和最大回撤持续时间。

USAGE: [maxDD maxDDD]=calculateMaxDD(cumret)
     calculation of maximum drawdown and maximum drawdown duration based on
     cumulative COMPOUNDED returns. cumret must be a compounded cumulative
     return.
     Same as calculateMaxDD_cpd for backward compatibility.
用法: [maxDD maxDDD]=calculateMaxDD(cumret)
     基于累计 COMPOUNDED 收益率计算最大回撤和最大回撤持续时间。
     cumret 必须是复利累计收益率。
     为保持向后兼容，与 calculateMaxDD_cpd 相同。

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com
编写者:
作者 Ernest Chan
著有《Quantitative Trading:
How to Start Your Own Algorithmic Trading Business?》一书。
"""

import numpy as np


def calculate_maxdd(cumret):
    """Return ``(maxDD, maxDDD)``: the maximum drawdown and its longest duration.

    计算最大回撤以及最大回撤的最长持续时间。
    """
    cumret = np.asarray(cumret, dtype=float).ravel()

    highwatermark = np.zeros_like(cumret)  # initialize high watermarks to zero.
    # 将高水位初始化为零。

    drawdown = np.zeros_like(cumret)  # initialize drawdowns to zero.
    # 将回撤初始化为零。

    drawdownduration = np.zeros_like(cumret)  # initialize drawdown duration to zero.
    # 将回撤持续时间初始化为零。

    for t in range(1, len(cumret)):
        highwatermark[t] = max(highwatermark[t - 1], cumret[t])
        # drawdown(t)=(1+cumret(t))./(1+highwatermark(t))-1; % drawdown on each day
        # 每日回撤
        # drawdown on each day
        # 每日回撤
        drawdown[t] = (1.0 + highwatermark[t]) / (1.0 + cumret[t]) - 1.0
        if drawdown[t] == 0:
            drawdownduration[t] = 0
        else:
            drawdownduration[t] = drawdownduration[t - 1] + 1

    max_dd = drawdown.max() if drawdown.size else np.nan  # maximum drawdown
    # 最大回撤

    # maximum drawdown duration
    # 最大回撤持续时间
    max_ddd = drawdownduration.max() if drawdownduration.size else np.nan
    return max_dd, max_ddd
