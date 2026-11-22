"""Port of the MATLAB ``getTday.m``.

Reads a spreadsheet whose first column holds the trading days (as Excel day
numbers) and whose last column holds the adjusted close prices.
读取一个电子表格文件: 第一列为交易日 (Excel 日期序列号),
最后一列为调整后的收盘价。
"""

import numpy as np

from .matlab_compat import excel_serial_to_yyyymmdd, xlsread


def get_tday(filename):
    """Return ``(tday, adjcls)`` for the spreadsheet ``filename``.

    ``tday`` is an array of ``yyyymmdd`` integers, ``adjcls`` the adjusted
    close prices (last column of the spreadsheet).
    返回 ``(tday, adjcls)``: ``tday`` 是 ``yyyymmdd`` 格式的整数数组,
    ``adjcls`` 是表格最后一列的调整后收盘价。
    """
    # xlsread returns the numeric block in num and the text cells in txt.
    # xlsread 把数值部分读入 num, 文本单元格读入 txt。
    num, _txt = xlsread(filename)
    # tday=num(1:end, 1); the trading days are in the first column.
    # tday=num(1:end, 1); 交易日位于第一列。
    tday = np.array([excel_serial_to_yyyymmdd(v) for v in num[:, 0]])
    # adjcls=num(:, end); the adjusted close prices are in the last column.
    # adjcls=num(:, end); 调整后收盘价位于最后一列。
    adjcls = num[:, -1]
    return tday, adjcls
