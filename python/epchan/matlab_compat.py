"""Helpers that emulate the handful of MATLAB builtins used by this project.

The MATLAB code relies on ``xlsread``, ``detrend``, ``intersect``, ``union``,
``sort`` and the matrix left division operator ``\\``.  They are re-implemented
here on top of numpy/scipy/xlrd so that the ported functions keep the exact
same semantics.
"""

import datetime as _dt

import numpy as np
import xlrd

#: Excel (and MATLAB ``datenum``) day zero used by ``xlsread`` output.
EXCEL_EPOCH = _dt.date(1899, 12, 30)


def xlsread(filename):
    """Read a spreadsheet the way MATLAB's ``xlsread`` does.

    MATLAB returns ``[num, txt]`` where ``num`` is the rectangular block of
    numeric cells and ``txt`` is the block of text cells found above/left of
    it.  Here ``num`` is a ``float64`` array (text cells inside the numeric
    block become ``NaN``) and ``txt`` is a list of lists of strings.

    Only the first worksheet is read, which is all the book needs.
    """
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)

    ctype_date = xlrd.XL_CELL_DATE
    ctype_number = xlrd.XL_CELL_NUMBER
    ctype_error = xlrd.XL_CELL_ERROR
    ctype_empty = xlrd.XL_CELL_EMPTY

    # Locate the first cell that holds a number (or a date): MATLAB skips the
    # leading text rows/columns of the used range.
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
    """Return the text of an xlrd cell (``''`` for numbers)."""
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
    """
    serial = float(serial)
    if not np.isfinite(serial):
        return np.nan
    day = EXCEL_EPOCH + _dt.timedelta(days=int(np.floor(serial)))
    return day.year * 10000 + day.month * 100 + day.day


def _excel_serial_to_yyyymmdd(serial):
    """Same as :func:`excel_serial_to_yyyymmdd` but returns a string."""
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
    """MATLAB's ``a \\ b`` for matrices: the least squares solution of ``a*x=b``."""
    a = np.atleast_2d(np.asarray(a, dtype=float))
    b = np.atleast_2d(np.asarray(b, dtype=float))
    x, _res, _rank, _sv = np.linalg.lstsq(a, b, rcond=None)
    return x


def sort_index(x, axis=None):
    """MATLAB's ``[s, idx] = sort(x)`` (stable sort, like MATLAB's)."""
    x = np.asarray(x)
    if axis is None:
        idx = np.argsort(x, kind="stable")
        return x[idx], idx
    idx = np.argsort(x, axis=axis, kind="stable")
    return np.take_along_axis(x, idx, axis=axis), idx


def _first_index_map(values):
    """Map each distinct value of ``values`` to the index of its 1st occurrence."""
    uniq, idx = np.unique(np.asarray(values).ravel(), return_index=True)
    return dict(zip(uniq.tolist(), idx.tolist()))


def intersect(a, b):
    """MATLAB's ``[c, ia, ib] = intersect(a, b)`` for 1-D arrays.

    The common values are returned in ascending order together with the
    indices of their first occurrence in ``a`` and in ``b``.
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
    """MATLAB's ``union(a, b)``: the sorted union of the distinct values."""
    return np.union1d(np.asarray(a).ravel(), np.asarray(b).ravel())


def matlab_round(x):
    """MATLAB's ``round``: halves are rounded away from zero.

    Python's builtin ``round`` uses banker's rounding, so ``round(12.5)`` is
    ``12`` in Python but ``13`` in MATLAB.
    """
    x = np.asarray(x, dtype=float)
    result = np.where(x >= 0, np.floor(x + 0.5), np.ceil(x - 0.5))
    if result.ndim == 0:
        return float(result)
    return result


def first_non_singleton_axis(x):
    """MATLAB's ``min(find(size(x)~=1))`` (1-based) expressed as a numpy axis."""
    shape = np.shape(x)
    for axis, size in enumerate(shape):
        if size != 1:
            return axis
    return 0
