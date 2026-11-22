"""Port of the MATLAB ``mprint.m`` written by James P. LeSage.

PURPOSE: print an (nobs x nvar) matrix in formatted form.
USAGE: mprint(y, info)
       where: y         = (nobs x nvar) matrix (or vector) to be printed
              info      = a structure containing printing options
              info.begr = beginning row to print,    (default = 1)
              info.endr = ending row to print,       (default = nobs)
              info.begc = beginning column to print, (default = 1)
              info.endc = ending column to print,    (default = nvar)
              info.cnames = an (nvar x 1) string vector of names for columns
                            (optional)
                            e.g. info.cnames = strvcat('col1','col2');
                            (default = no column headings)
              info.rnames = an (nobs+1 x 1) string vector of names for rows
                            (optional)
                            e.g. info.rnames = strvcat('Rows','row1','row2');
                            (default = no row labels)
              info.fmt    = a format string, e.g., '%12.6f' or '%12d'
                            (default = %10.4f)
                            or an (nvar x 1) string containing formats
                            e.g., info.fmt=strvcat('%12.6f','%12.2f','%12d');
                            for nvar = 3
              info.fid    = file-id for printing results to a file
                            (defaults to the MATLAB command window)
                            e.g. fid = fopen('file.out','w');
              info.rflag  = 1 for row #'s printed, 0 for no row #'s
                            (default = 0)
              info.width  = # of columns before wrapping occurs
                            (default = 80)
NOTES: - defaults are used for info-elements not specified
       - default wrapping occurs at 80 columns, which varies depending on the
         format you use, e.g. %10.2f will wrap after 8 columns
SEE ALSO: tsprint, mprint_d, lprint
用途: 以格式化形式打印 (nobs x nvar) 矩阵
用法: mprint(y, info)
      其中: y = 需要打印的 (nobs x nvar) 矩阵（或向量）
             info = 包含打印选项的结构体
             info.begr = 打印的起始行, (默认值 = 1)
             info.endr = 打印的结束行, (默认值 = nobs)
             info.begc = 打印的起始列, (默认值 = 1
             info.endc = 打印的结束列, (默认值 = nvar)
             info.cnames = 列名的 (nvar x 1) 字符串向量（可选）
             例如 info.cnames = strvcat('col1','col2');
             (默认值 = 无列标题)
             info.rnames = 行名的 (nobs+1 x 1) 字符串向量（可选）
             例如 info.rnames = strvcat('Rows','row1','row2');
             (默认值 = 无行标签)
             info.fmt = 格式字符串, 例如 '%12.6f' 或 '%12d' (默认值 = %10.4f)
             或为包含各格式的 (nvar x 1) 字符串
             例如, info.fmt=strvcat('%12.6f','%12.2f','%12d'); 当 nvar = 3
             info.fid = 将结果打印到文件所用的 file-id
             (默认输出到 MATLAB 命令窗口)
             例如 fid = fopen('file.out','w');
             info.rflag = 1 表示打印行号, 0 表示不打印行号 (默认值 = 0)
             info.width = 发生换行前的列数 (默认值 = 80)
参见: tsprint, mprint_d, lprint

e.g.   in.cnames = strvcat('col1','col2');
       in.rnames = strvcat('rowlabel','row1','row2');
       mprint(y,in), prints entire matrix, column and row headings
       in2.endc = 3; in2.cnames = strvcat('col1','col2','col3');
    or: mprint(y,in2), prints 3 columns of the matrix, just column headings
    or: mprint(y), prints entire matrix, no column headings or row labels
例如 in.cnames = strvcat('col1','col2');
例如 in.rnames = strvcat('rowlabel','row1','row2');
mprint(y,in), 打印整个矩阵, 包含列标题和行标题
例如 in2.endc = 3; in2.cnames = strvcat('col1','col2','col3');
或: mprint(y,in2), 打印矩阵的 3 列, 仅有列标题
或: mprint(y), 打印整个矩阵, 无列标题和行标签

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jpl@jpl.econ.utoledo.edu
编写者:

Prints an ``(nobs x nvar)`` matrix in a formatted way, with optional column
headings, row labels and per column format strings.
以格式化方式打印 ``(nobs x nvar)`` 矩阵，可选地带上列标题、行标签以及
逐列的格式字符串。
"""

import sys

import numpy as np


def _parse_format(fmt):
    """Parse a MATLAB format string.

    Returns ``(width, decimals, kind)`` where ``kind`` is one of ``'f'``,
    ``'d'`` or ``'s'``.

    The original MATLAB code parses the format strings with ``strtok``; when
    the ``%`` is missing (as in the ``'16.8f'`` used by ``prt_coint``) that
    parser goes haywire and the column is printed with the wrong number of
    decimals.  Here the ``%`` is simply added back when it is missing, which
    restores the output shown in the book.

    解析 MATLAB 的格式字符串。

    返回 ``(width, decimals, kind)``，其中 ``kind`` 是 ``'f'``、``'d'``
    或 ``'s`` 之一。

    原始 MATLAB 代码用 ``strtok`` 解析格式字符串；当 ``%`` 缺失时
    （例如 ``prt_coint`` 使用的 ``'16.8f'``），该解析器会出错，导致该列
    按错误的小数位数打印。这里只是在 ``%`` 缺失时把它补回去，从而恢复
    书中所展示的输出。
    """
    s = str(fmt).strip()
    if not s.startswith("%"):
        s = "%" + s
    body = s[1:]
    if body.endswith("d") or body.endswith("i"):
        return int(body[:-1] or 0), 0, "d"
    if body.endswith(("f", "e", "g")):
        if "." in body:
            head, _sep, tail = body[:-1].partition(".")
            return int(head or 0), int(tail), "f"
        return int(body[:-1] or 0), 6, "f"
    if body.endswith("s"):
        return int(body[:-1] or 0), 0, "s"
    return int(body or 0), 0, "s"


def _format_value(value, width, decimals, kind):
    """Format a single value the way MATLAB's ``fprintf`` would.

    按照 MATLAB 的 ``fprintf`` 的方式格式化单个数值。
    """
    if kind == "d":
        return "%*d" % (width, int(round(float(value))))
    if kind == "s":
        return "%*s" % (width, str(value))
    return "%*.*f" % (width, decimals, float(value))


def mprint(y, info=None, fid=None):
    """Print the matrix ``y``.

    ``info`` is a dictionary that may contain the following keys (the MATLAB
    field names are kept):

    ``fmt``
        a format string such as ``'%12.6f'`` or a list with one format per
        column (default ``'%10.4f'``),
    ``fid``
        the file object the output is written to (default ``sys.stdout``),
    ``begc``/``endc``
        first/last column to print (default ``1``/``nvars``),
    ``begr``/``endr``
        first/last row to print (default ``1``/``nobs``),
    ``width``
        number of columns before the output wraps (default ``80``),
    ``cnames``
        list with the heading of every column,
    ``rnames``
        list with the heading of every row plus one extra label,
    ``rflag``
        print the row numbers when ``1``.

    打印矩阵 ``y``。

    ``info`` 是一个字典，可以包含以下这些键（沿用 MATLAB 的字段名）：

    ``fmt``
        格式字符串，例如 ``'%12.6f'``，或每列一个格式的列表
        （默认 ``'%10.4f'``），
    ``fid``
        输出写入的文件对象（默认 ``sys.stdout``），
    ``begc``/``endc``
        打印的第一列/最后一列（默认 ``1``/``nvars``），
    ``begr``/``endr``
        打印的第一行/最后一行（默认 ``1``/``nobs``），
    ``width``
        输出换行之前的列数（默认 ``80``），
    ``cnames``
        每一列标题的列表，
    ``rnames``
        每一行标题的列表，另加一个额外的标签，
    ``rflag``
        当为 ``1`` 时打印行号。
    """
    y = np.asarray(y, dtype=float)
    if y.ndim == 1:
        y = y.reshape(-1, 1)

    if fid is None:
        fid = sys.stdout
    if info is None:
        info = {}
    if isinstance(info, dict) and "fid" in info and info["fid"] is not None:
        fid = info["fid"]

    # Setup defaults.
    # 设置默认值。
    nobs, nvars = y.shape
    begr = int(info.get("begr", 1))
    endr = int(info.get("endr", nobs))
    begc = int(info.get("begc", 1))
    endc = int(info.get("endc", nvars))
    cwidth = int(info.get("width", 80))

    fmt = info.get("fmt", "%10.4f")
    if isinstance(fmt, str):
        fmts = [fmt]
    else:
        fmts = list(fmt)
    nfmts = len(fmts)
    if nfmts not in (1, nvars):
        raise ValueError("mprint: wrong # of formats in string -- need nvar")

    # See if the user supplied row names and set rnum; correct her mistake
    # if she did this.
    # 检查用户是否提供了行名并设置 rnum；如果用户这样做了，就纠正她的错误。
    cnames = info.get("cnames")
    rnames = info.get("rnames")
    rflag = 1 if rnames is not None else 0
    rnum = int(info.get("rflag", 0)) if rflag == 0 else 0
    if rflag == 1:
        rnum = 0

    if cnames is not None:
        if len(cnames) != nvars:
            raise ValueError("Wrong # cnames in mprint")
    if rnames is not None and len(rnames) != nobs + 1:
        raise ValueError("Wrong # rnames in mprint")

    # Parse the formats and work out how many columns fit on one line.
    # 解析格式，并算出每一行能容纳多少列。
    parsed = [_parse_format(fmts[0] if nfmts == 1 else fmts[i])
              for i in range(nvars)]
    if nfmts == 1:
        nwide = max(cwidth // max(parsed[0][0], 1), 1)
    else:
        # MATLAB uses the widest ``nwide`` (i.e. the narrowest format) when
        # several format strings are supplied.
        # 当提供多个格式字符串时，MATLAB 使用最大的 ``nwide``
        #（也就是最窄的格式）。
        nwide = max(max(cwidth // max(p[0], 1), 1) for p in parsed)
    nvar = endc - begc + 1
    nsets = int(np.ceil(nvar / nwide)) if nvar > 0 else 0

    # Width of the heading of each column (never narrower than the format).
    # 每一列标题的宽度（不会小于格式宽度）。
    if cnames is not None:
        # MATLAB builds the headings from a fixed width string matrix, so every
        # heading is padded to the widest name (or its own format width).
        # MATLAB 用固定宽度的字符串矩阵来构造标题，因此每个标题都会补齐
        # 到最宽的名称（或其自身的格式宽度）。
        widest_name = max(len(str(c)) for c in cnames)
        name_widths = [max(parsed[i][0], widest_name) for i in range(nvars)]
    else:
        name_widths = [parsed[i][0] for i in range(nvars)]

    row_label_width = 0
    if rflag == 1:
        row_label_width = max(len(str(r)) for r in rnames)

    # Print matrix.
    # 打印矩阵。
    out = []
    for j in range(nsets):
        first = begc + j * nwide
        last = min(first + nwide, endc + 1)

        # Header.
        # 表头。
        # MATLAB guards the right justification of the column names with a
        # version check, which is left commented out in the original:
        # MATLAB 用一个版本检查来决定列名是否右对齐，原文件中该检查被注释掉了:
        # [version,junk] = version; vers = str2num(version);
        header = ""
        if rnum == 1:
            header += "%5s " % "Obs#"
        elif rflag == 1:
            header += "%*s " % (row_label_width, rnames[0])
        if cnames is not None:
            for i in range(first, last):
                header += "%*s " % (name_widths[i - 1], cnames[i - 1])
        out.append(header)

        # Data.
        # 数据。
        for k in range(begr, endr + 1):
            line = ""
            if rnum == 1:
                line += "%5d " % k
            elif rflag == 1:
                line += "%*s " % (row_label_width, rnames[k])
            for i in range(first, last):
                width, decimals, kind = parsed[i - 1]
                line += _format_value(y[k - 1, i - 1], width, decimals, kind) + " "
            out.append(line)
        out.append("")

    text = "\n".join(out) + "\n"
    fid.write(text)
    return text
