"""Port of the MATLAB ``isLastTradingDayOfMonth.m`` written by Ernest Chan."""

import numpy as np

from .fwdshift import fwdshift


def is_last_trading_day_of_month(tday):
    """Return a boolean array: ``True`` where ``tday`` is a month end.

    ``tday`` holds ``yyyymmdd`` numbers.  A day is a month end when the month
    of the day differs from the month of the next trading day.
    """
    tday = np.asarray(tday, dtype=float)
    today_month = np.fix(np.mod(tday, 10000) / 100)
    tmr_month = fwdshift(1, today_month)
    is_last = (today_month != tmr_month) & np.isfinite(today_month) & np.isfinite(tmr_month)
    return is_last
