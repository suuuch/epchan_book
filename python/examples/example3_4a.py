"""Port of ``example3_4a.m``: IGE against SPY, a market neutral strategy.
``example3_4a.m`` 的 Python 移植：IGE 对 SPY，市场中性策略。

The book says the Sharpe ratio should be 0.7618 for IGE alone and 0.7837 for
the market neutral portfolio.
书中给出的夏普比率：单独持有 IGE 为 0.7618，市场中性组合为 0.7837。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.matlab_compat import excel_serial_to_yyyymmdd, sort_index, xlsread
from epchan.paths import data_path


def _read_adjusted_close(filename):
    """Read a spreadsheet and return the adjusted close prices sorted by date.
    读取电子表格，并返回按日期排序的复权收盘价。
    """
    num, _txt = xlsread(filename)
    # the first column (starting from the second row) contains the trading days
    # in format mm/dd/yyyy.
    # 第一列（从第二行开始）包含 mm/dd/yyyy 格式的交易日。
    tday = np.array([excel_serial_to_yyyymmdd(v) for v in num[:, 0]])
    # the last column contains the adjusted close prices.
    # 最后一列包含复权收盘价。
    cls = num[:, -1]
    # sort tday into ascending order.
    # 将 tday 按升序排序。
    _sorted_tday, sort_index_ = sort_index(tday)
    # sort cls into ascending order of dates.
    # 按日期升序排列 cls。
    return cls[sort_index_]


def main():
    # read a spreadsheet named "IGE.xls" into MATLAB.
    # 将名为 "IGE.xls" 的电子表格读入 MATLAB。
    cls = _read_adjusted_close(data_path("IGE.xls"))

    dailyret = (cls[1:] - cls[:-1]) / cls[:-1]  # daily returns
    # 日收益率

    # excess daily returns = strategy returns - financing cost, assuming a
    # risk-free rate of 4% per annum and 252 trading days in a year
    # 超额日收益率 = 策略收益率 - 融资成本，假设年化无风险利率为 4%，
    # 一年有 252 个交易日
    excess_ret = dailyret - 0.04 / 252
    sharpe_ratio = np.sqrt(252) * excess_ret.mean() / excess_ret.std()
    # the output should be 0.7618
    # 输出结果应为 0.7618
    print("sharpeRatio (IGE)        = %.4f   (the book says 0.7618)" % sharpe_ratio)

    # read a spreadsheet named "SPY.xls" into MATLAB.
    # 将名为 "SPY.xls" 的电子表格读入 MATLAB。
    cls = _read_adjusted_close(data_path("SPY.xls"))
    dailyret_spy = (cls[1:] - cls[:-1]) / cls[:-1]  # daily returns
    # 日收益率

    # net daily returns (divide by 2 because we now have twice as much capital)
    # 净日收益率（除以 2，因为现在的资金量是原来的两倍。）
    net_ret = (dailyret - dailyret_spy) / 2
    sharpe_ratio = np.sqrt(252) * net_ret.mean() / net_ret.std()
    # the output should be 0.7837
    # 输出结果应为 0.7837
    print("sharpeRatio (IGE vs SPY) = %.4f   (the book says 0.7837)" % sharpe_ratio)
    return sharpe_ratio


if __name__ == "__main__":
    main()
