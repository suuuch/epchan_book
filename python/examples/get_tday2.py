"""Port of ``getTday2.asv``.

``.asv`` is MATLAB's AutoSave extension, and the saved draft contains a syntax
error (``tmp1(k) = mod(tday(k),1000;`` has a missing closing parenthesis), so
the original function never ran.  The evident intent was to turn ``yyyymmdd``
day numbers into MATLAB date strings; this port does exactly that and returns
the dates formatted the way ``datestr`` formats them by default
(``dd-mmm-yyyy``).
"""

import datetime as _dt

import numpy as np


def get_tday2(tday):
    """Convert ``yyyymmdd`` day numbers into ``dd-mmm-yyyy`` strings.

    ``tday`` may be a scalar, a list or an array; a list of strings is always
    returned, mirroring ``cellstr(datestr(...))``.
    """
    values = np.atleast_1d(np.asarray(tday)).ravel()
    out = []
    for value in values:
        value = int(value)
        try:
            day = _dt.date(value // 10000, (value // 100) % 100, value % 100)
        except ValueError:
            out.append("")
            continue
        out.append(day.strftime("%d-%b-%Y"))
    return out


def main():
    """Print a small demonstration, mirroring the script-like ``.asv`` file."""
    values = [20071123, 20051130]
    print(get_tday2(values))
    return get_tday2(values)


if __name__ == "__main__":
    main()
