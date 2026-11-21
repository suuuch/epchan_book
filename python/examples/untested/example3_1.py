"""Port of ``untested/example3_1.m``: scrape historical prices from Yahoo.

.. note::

   The MATLAB original parses the HTML of
   ``http://finance.yahoo.com/q/hp?s=IBM``.  That page and its markup no
   longer exist (Yahoo retired it around 2017), so this script is kept as a
   faithful translation of the original logic but cannot be expected to
   produce data today.  Use the CSV exports bundled with the book instead.
"""

import sys
from pathlib import Path
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import re

import numpy as np


def main():
    symbol = "IBM"  # the stock of interest

    # retrieving a webpage
    url = "http://finance.yahoo.com/q/hp?s=%s" % symbol
    with urlopen(url, timeout=30) as response:
        historical_price_file = response.read().decode("utf-8", errors="replace")

    # extracting the date field to a list
    date_field = re.findall(
        r'<td class="yfnc_tabledata1" nowrap align="right">([\d\w-]+)</td>',
        historical_price_file)

    # extracting the numbers field to a list
    num_field = re.findall(
        r'<td class="yfnc_tabledata1" align="right">([\d.,]+)</td>',
        historical_price_file)

    # convert to doubles array
    op = _str2double(num_field[0::6])    # open
    hi = _str2double(num_field[1::6])    # high
    lo = _str2double(num_field[2::6])    # low
    cl = _str2double(num_field[3::6])    # close
    vol = _str2double(num_field[4::6])   # volume
    adj_cl = _str2double(num_field[5::6])  # adjusted close

    print("dates %d, open %d, high %d, low %d, close %d, volume %d, adj close %d"
          % (len(date_field), len(op), len(hi), len(lo), len(cl), len(vol), len(adj_cl)))
    return date_field, op, hi, lo, cl, vol, adj_cl


def _str2double(values):
    """MATLAB's ``str2double`` applied element wise (commas are removed)."""
    return np.array([float(v.replace(",", "")) for v in values])


if __name__ == "__main__":
    main()
