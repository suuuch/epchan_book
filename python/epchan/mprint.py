"""Port of the MATLAB ``mprint.m`` written by James P. LeSage.

Prints an ``(nobs x nvar)`` matrix in a formatted way, with optional column
headings, row labels and per column format strings.
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
    """Format a single value the way MATLAB's ``fprintf`` would."""
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
    parsed = [_parse_format(fmts[0] if nfmts == 1 else fmts[i])
              for i in range(nvars)]
    if nfmts == 1:
        nwide = max(cwidth // max(parsed[0][0], 1), 1)
    else:
        # MATLAB uses the widest ``nwide`` (i.e. the narrowest format) when
        # several format strings are supplied.
        nwide = max(max(cwidth // max(p[0], 1), 1) for p in parsed)
    nvar = endc - begc + 1
    nsets = int(np.ceil(nvar / nwide)) if nvar > 0 else 0

    # Width of the heading of each column (never narrower than the format).
    if cnames is not None:
        # MATLAB builds the headings from a fixed width string matrix, so every
        # heading is padded to the widest name (or its own format width).
        widest_name = max(len(str(c)) for c in cnames)
        name_widths = [max(parsed[i][0], widest_name) for i in range(nvars)]
    else:
        name_widths = [parsed[i][0] for i in range(nvars)]

    row_label_width = 0
    if rflag == 1:
        row_label_width = max(len(str(r)) for r in rnames)

    out = []
    for j in range(nsets):
        first = begc + j * nwide
        last = min(first + nwide, endc + 1)

        # Header.
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
