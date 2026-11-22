"""Helpers that emulate the handful of MATLAB builtins used by this project.

The MATLAB code relies on ``xlsread``, ``detrend``, ``intersect``, ``union``,
``sort`` and the matrix left division operator ``\\``.  They are re-implemented
here on top of numpy/scipy/xlrd so that the ported functions keep the exact
same semantics.
本项目使用的一些 MATLAB 内置函数被重新实现于此。MATLAB 代码依赖
``xlsread``、``detrend``、``intersect``、``union``、``sort`` 以及矩阵左除
运算符 ``\\``。这里基于 numpy/scipy/xlrd 重新实现了它们，从而让移植后的
函数保持完全相同的语义。

PURPOSE: Emulate the MATLAB builtins that the ported functions rely on:
         xlsread, detrend, intersect, union, sort and the matrix left
         division operator '\\'.
---------------------------------------------------
USAGE: num, txt = xlsread(filename)
       x = detrend(x, p)
       [c, ia, ib] = intersect(a, b)
       c = union(a, b)
       [s, idx] = sort_index(x, axis)
       x = left_divide(a, b)
---------------------------------------------------
RETURNS: the same values as the corresponding MATLAB builtins, so that the
         ported functions keep the exact same semantics.
---------------------------------------------------
用途: 模拟移植后的函数所依赖的 MATLAB 内置函数：xlsread、detrend、
      intersect、union、sort 以及矩阵左除运算符 '\\'。
---------------------------------------------------
用法: num, txt = xlsread(filename)
      x = detrend(x, p)
      [c, ia, ib] = intersect(a, b)
      c = union(a, b)
      [s, idx] = sort_index(x, axis)
      x = left_divide(a, b)
---------------------------------------------------
返回: 与相应的 MATLAB 内置函数相同的值，从而保证移植后的函数
      具有完全一致的语义。
"""

import datetime as _dt

import numpy as np
import xlrd

#: Excel (and MATLAB ``datenum``) day zero used by ``xlsread`` output.
#: ``xlsread`` 输出所用的 Excel（以及 MATLAB ``datenum``）零日。
EXCEL_EPOCH = _dt.date(1899, 12, 30)


def xlsread(filename):
    """Read a spreadsheet the way MATLAB's ``xlsread`` does.

    MATLAB returns ``[num, txt]`` where ``num`` is the rectangular block of
    numeric cells and ``txt`` is the block of text cells found above/left of
    it.  Here ``num`` is a ``float64`` array (text cells inside the numeric
    block become ``NaN``) and ``txt`` is a list of lists of strings.

    Only the first worksheet is read, which is all the book needs.

    以 MATLAB 的 ``xlsread`` 的方式读取电子表格。

    MATLAB 返回 ``[num, txt]``，其中 ``num`` 是数值单元格的矩形块，``txt``
    是位于其上方/左方的文本单元格块。这里 ``num`` 是 ``float64`` 数组
    （数值块内部的文本单元格变为 ``NaN``），``txt`` 是字符串的二维列表。

    只读取第一个工作表，这也是本书所需的全部内容。
    """
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)

    ctype_date = xlrd.XL_CELL_DATE
    ctype_number = xlrd.XL_CELL_NUMBER
    ctype_error = xlrd.XL_CELL_ERROR
    ctype_empty = xlrd.XL_CELL_EMPTY

    # Locate the first cell that holds a number (or a date): MATLAB skips the
    # leading text rows/columns of the used range.
    # 定位第一个存放数值（或日期）的单元格：MATLAB 会跳过已用区域前面的
    # 文本行/文本列。
    first_row = first_col = None
    for r in range(sheet.nrows):
        for c in range(sheet.ncols):
            if sheet.cell_type(r, c) in (ctype_number, ctype_date):
                first_row, first_col = r, c
                break
        if first_row is not None:
            break
    if first_row is None:
        return np.zeros((0, 0)), []

    # The text block sits above and to the left of the numeric block.
    # 文本块位于数值块的上方和左方。
    txt = [[_cell_text(sheet.cell(r, c)) for c in range(first_col)]
           for r in range(first_row)]

    num = np.full((sheet.nrows - first_row, sheet.ncols - first_col), np.nan)
    for r in range(first_row, sheet.nrows):
        for c in range(first_col, sheet.ncols):
            cell = sheet.cell(r, c)
            if cell.ctype in (ctype_number, ctype_date):
                num[r - first_row, c - first_col] = float(cell.value)
            elif cell.ctype in (ctype_empty, ctype_error):
                num[r - first_row, c - first_col] = np.nan

    return num, txt


def _cell_text(cell):
    """Return the text of an xlrd cell (``''`` for numbers).

    返回 xlrd 单元格的文本（对数值返回 ``''``）。
    """
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        return ""
    if cell.ctype == xlrd.XL_CELL_TEXT:
        return cell.value
    if cell.ctype == xlrd.XL_CELL_DATE:
        return _excel_serial_to_yyyymmdd(cell.value)
    return str(cell.value)


def excel_serial_to_yyyymmdd(serial):
    """Convert an Excel day number into a ``yyyymmdd`` integer.

    This is the Python equivalent of MATLAB's

        datestr(serial + datenum('30-Dec-1899'), 'yyyymmddTHHMMSS')

    which is what the original scripts use to turn the first column of the
    spreadsheets into a sortable numeric date.

    将 Excel 的日期序号转换为 ``yyyymmdd`` 整数。

    它相当于 MATLAB 的

        datestr(serial + datenum('30-Dec-1899'), 'yyyymmddTHHMMSS')

    原始脚本正是用它把电子表格的第一列变成可排序的数值型日期。
    """
    serial = float(serial)
    if not np.isfinite(serial):
        return np.nan
    day = EXCEL_EPOCH + _dt.timedelta(days=int(np.floor(serial)))
    return day.year * 10000 + day.month * 100 + day.day


def _excel_serial_to_yyyymmdd(serial):
    """Same as :func:`excel_serial_to_yyyymmdd` but returns a string.

    与 :func:`excel_serial_to_yyyymmdd` 相同，但返回字符串。
    """
    value = excel_serial_to_yyyymmdd(serial)
    if not np.isfinite(value):
        return ""
    return "%08d" % int(value)


def detrend(x, p=0):
    """MATLAB's ``detrend(x, p)``.

    * ``p == 0`` removes the mean of every column,
    * ``p >= 1`` removes the least squares polynomial trend of degree ``p``,
    * ``p == -1`` keeps the data untouched ("no deterministic part"), which is
      how ``cadf`` interprets a negative order of the time polynomial.

    MATLAB 的 ``detrend(x, p)``。

    * ``p == 0`` 去除每一列的均值，
    * ``p >= 1`` 去除 ``p`` 阶最小二乘多项式趋势，
    * ``p == -1`` 保持数据原样（"无确定性部分"），``cadf`` 正是这样解释
      时间多项式阶数为负的情形。
    """
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    if p == -1:
        return x.copy()
    if p == 0:
        return x - x.mean(axis=0)
    nobs = x.shape[0]
    t = np.arange(1.0, nobs + 1.0)
    design = np.vander(t, p + 1, increasing=True)
    coef, _res, _rank, _sv = np.linalg.lstsq(design, x, rcond=None)
    return x - design @ coef


def left_divide(a, b):
    """MATLAB's ``a \\ b`` for matrices: the least squares solution of ``a*x=b``.

    MATLAB 中矩阵的 ``a \\ b``：``a*x=b`` 的最小二乘解。
    """
    a = np.atleast_2d(np.asarray(a, dtype=float))
    b = np.atleast_2d(np.asarray(b, dtype=float))
    x, _res, _rank, _sv = np.linalg.lstsq(a, b, rcond=None)
    return x


def sort_index(x, axis=None):
    """MATLAB's ``[s, idx] = sort(x)`` (stable sort, like MATLAB's).

    MATLAB 的 ``[s, idx] = sort(x)``（稳定排序，与 MATLAB 一致）。
    """
    x = np.asarray(x)
    if axis is None:
        idx = np.argsort(x, kind="stable")
        return x[idx], idx
    idx = np.argsort(x, axis=axis, kind="stable")
    return np.take_along_axis(x, idx, axis=axis), idx


def _first_index_map(values):
    """Map each distinct value of ``values`` to the index of its 1st occurrence.

    将 ``values`` 中每个不同的值映射到其首次出现的索引。
    """
    uniq, idx = np.unique(np.asarray(values).ravel(), return_index=True)
    return dict(zip(uniq.tolist(), idx.tolist()))


def intersect(a, b):
    """MATLAB's ``[c, ia, ib] = intersect(a, b)`` for 1-D arrays.

    The common values are returned in ascending order together with the
    indices of their first occurrence in ``a`` and in ``b``.

    MATLAB 中针对一维数组的 ``[c, ia, ib] = intersect(a, b)``。

    共同的值按升序返回，同时给出它们在 ``a`` 和 ``b`` 中首次出现的索引。
    """
    a = np.asarray(a).ravel()
    b = np.asarray(b).ravel()
    common = np.intersect1d(a, b)
    map_a = _first_index_map(a)
    map_b = _first_index_map(b)
    ia = np.array([map_a[v] for v in common.tolist()], dtype=int)
    ib = np.array([map_b[v] for v in common.tolist()], dtype=int)
    return common, ia, ib


def union(a, b):
    """MATLAB's ``union(a, b)``: the sorted union of the distinct values.

    MATLAB 的 ``union(a, b)``：不同取值的有序并集。
    """
    return np.union1d(np.asarray(a).ravel(), np.asarray(b).ravel())


def matlab_round(x):
    """MATLAB's ``round``: halves are rounded away from zero.

    Python's builtin ``round`` uses banker's rounding, so ``round(12.5)`` is
    ``12`` in Python but ``13`` in MATLAB.

    MATLAB 的 ``round``：恰好处于中间的数向远离零的方向取整。

    Python 内置的 ``round`` 采用银行家舍入，因此 ``round(12.5)`` 在 Python
    中为 ``12``，而在 MATLAB 中为 ``13``。
    """
    x = np.asarray(x, dtype=float)
    result = np.where(x >= 0, np.floor(x + 0.5), np.ceil(x - 0.5))
    if result.ndim == 0:
        return float(result)
    return result


def first_non_singleton_axis(x):
    """MATLAB's ``min(find(size(x)~=1))`` (1-based) expressed as a numpy axis.

    MATLAB 的 ``min(find(size(x)~=1))``（以 1 为起点）用 numpy 的轴表示；
    注意 numpy 的轴是以 0 为起点的。

    MATLAB 中 ``dim`` 的 1 起始编号在 numpy 中变为 0 起始的 ``axis``。
    """
    shape = np.shape(x)
    for axis, size in enumerate(shape):
        if size != 1:
            return axis
    return 0
