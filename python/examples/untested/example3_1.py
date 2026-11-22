"""Port of ``untested/example3_1.m``: scrape historical prices from Yahoo.
``untested/example3_1.m`` 的 Python 移植：从 Yahoo 抓取历史行情。

.. note::

   The MATLAB original parses the HTML of
   ``http://finance.yahoo.com/q/hp?s=IBM``.  That page and its markup no
   longer exist (Yahoo retired it around 2017), so this script is kept as a
   faithful translation of the original logic but cannot be expected to
   produce data today.  Use the CSV exports bundled with the book instead.

   MATLAB 原始版本解析 ``http://finance.yahoo.com/q/hp?s=IBM`` 返回的 HTML。
   该页面及其标记如今已不存在（Yahoo 大约在 2017 年下线了该页面），因此本脚本
   忠实保留了原始逻辑，但今天不应指望它能取到数据。请改用书中自带的 CSV 导出文件。

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com

编写者:
Ernest Chan，《Quantitative Trading: How to Start Your Own Algorithmic Trading
Business》一书的作者
"""

import sys
from pathlib import Path
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import re

import numpy as np


def main():
    """Scrape the historical prices of one symbol from the Yahoo quote page.
    从 Yahoo 行情页面抓取某一个标的的历史价格。
    """
    symbol = "IBM"  # the stock of interest
    # 关注的股票

    # retrieving a webpage
    # 获取网页
    url = "http://finance.yahoo.com/q/hp?s=%s" % symbol
    with urlopen(url, timeout=30) as response:
        historical_price_file = response.read().decode("utf-8", errors="replace")

    # extracting the date field to a list
    # 将日期字段提取到一个列表中
    date_field = re.findall(
        r'<td class="yfnc_tabledata1" nowrap align="right">([\d\w-]+)</td>',
        historical_price_file)

    # extracting the numbers field to a list
    # 将数字字段提取到一个列表中
    num_field = re.findall(
        r'<td class="yfnc_tabledata1" align="right">([\d.,]+)</td>',
        historical_price_file)

    # convert to doubles array
    # 转换为双精度数组
    op = _str2double(num_field[0::6])    # open
    # 开盘价
    hi = _str2double(num_field[1::6])    # high
    # 最高价
    lo = _str2double(num_field[2::6])    # low
    # 最低价
    cl = _str2double(num_field[3::6])    # close
    # 收盘价
    vol = _str2double(num_field[4::6])   # volume
    # 成交量
    adj_cl = _str2double(num_field[5::6])  # adjusted close
    # 复权收盘价

    print("dates %d, open %d, high %d, low %d, close %d, volume %d, "
          "adj close %d"
          % (len(date_field), len(op), len(hi), len(lo), len(cl), len(vol),
             len(adj_cl)))
    return date_field, op, hi, lo, cl, vol, adj_cl


def _str2double(values):
    """MATLAB's ``str2double`` applied element wise (commas are removed).
    逐元素应用 MATLAB 的 ``str2double``（先去掉逗号）。
    """
    return np.array([float(v.replace(",", "")) for v in values])


if __name__ == "__main__":
    main()
