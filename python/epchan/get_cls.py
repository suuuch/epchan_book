"""Port of the MATLAB ``getCls.m``.

Same as :func:`epchan.get_tday` but the prices are sorted by ascending date.
与 :func:`epchan.get_tday` 相同, 但价格按日期升序排序。
"""

import numpy as np

from .matlab_compat import excel_serial_to_yyyymmdd, sort_index, xlsread


def get_cls(filename):
    """Return the adjusted close prices of ``filename`` sorted by date.

    返回 ``filename`` 中按日期升序排列的调整后收盘价。
    """
    # xlsread returns the numeric block in num and the text cells in txt.
    # xlsread 把数值部分读入 num, 文本单元格读入 txt。
    num, _txt = xlsread(filename)
    # tday=num(1:end, 1); the trading days are in the first column.
    # tday=num(1:end, 1); 交易日位于第一列。
    tday = np.array([excel_serial_to_yyyymmdd(v) for v in num[:, 0]])
    # cls=num(:, end); the adjusted close prices are in the last column.
    # cls=num(:, end); 调整后收盘价位于最后一列。
    cls = num[:, -1]
    # [tday sortIndex]=sort(tday); sort the rows by ascending date.
    # [tday sortIndex]=sort(tday); 按日期升序对各行排序。
    _sorted_tday, sort_index_ = sort_index(tday)
    return cls[sort_index_]
