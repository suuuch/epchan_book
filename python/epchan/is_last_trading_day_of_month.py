"""Port of the MATLAB ``isLastTradingDayOfMonth.m`` written by Ernest Chan.

isLastTradingDayOfMonth=isLastTradingDayOfMonth(tday) returns a logical
array. True if tday(t) is last trading day of month.
isLastTradingDayOfMonth=isLastTradingDayOfMonth(tday) 返回一个逻辑数组。
若 tday(t) 是该月最后一个交易日, 则为真。

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

from .fwdshift import fwdshift


def is_last_trading_day_of_month(tday):
    """Return a boolean array: ``True`` where ``tday`` is a month end.

    ``tday`` holds ``yyyymmdd`` numbers.  A day is a month end when the month
    of the day differs from the month of the next trading day.
    返回一个布尔数组: ``tday`` 为月末交易日的元素取 ``True``。

    ``tday`` 保存 ``yyyymmdd`` 格式的数字。当某一天的月份与其后一个交易日
    的月份不同时, 该天即为月末。
    """
    tday = np.asarray(tday, dtype=float)
    #tdayStr=datestr(datenum(num2str(tday), 'yyyymmdd'));
    # tdayStr=datestr(datenum(num2str(tday), 'yyyymmdd'));（已注释掉的语句）

    #todayMonth=month(tdayStr);
    # todayMonth=month(tdayStr);（已注释掉的语句）
    today_month = np.fix(np.mod(tday, 10000) / 100)

    tmr_month = fwdshift(1, today_month)  # tomorrow's month
    # 下一个月的月份

    is_last = (
        (today_month != tmr_month)
        & np.isfinite(today_month)
        & np.isfinite(tmr_month)
    )
    return is_last
