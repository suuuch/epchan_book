"""Port of ``example3_4.m``: the Sharpe ratio of the IGE ETF.
``example3_4.m`` 的 Python 移植：计算 IGE ETF 的夏普比率。

The book says the output should be 0.7893.
书中给出的输出结果应为 0.7893。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.matlab_compat import excel_serial_to_yyyymmdd, sort_index, xlsread
from epchan.paths import data_path


def main():
    # read a spreadsheet named "IGE.xls" into MATLAB.
    # 将名为 "IGE.xls" 的电子表格读入 MATLAB。
    num, _txt = xlsread(data_path("IGE.xls"))

    # In MATLAB this is done with tday=str2double(cellstr(tday)), which converts
    # the date strings first into cell arrays and then into numeric format.
    # MATLAB 中用 tday=str2double(cellstr(tday)) 完成，即先将日期字符串转换为
    # 单元格数组，然后再转换为数值格式。
    tday = np.array([excel_serial_to_yyyymmdd(v) for v in num[:, 0]])

    cls = num[:, -1]  # the last column contains the adjusted close prices.
    # 最后一列包含复权收盘价。

    _sorted_tday, sort_index_ = sort_index(tday)  # sort tday into ascending order.
    # 将 tday 按升序排序。
    cls = cls[sort_index_]  # sort cls into ascending order of dates.
    # 按日期升序排列 cls。

    dailyret = (cls[1:] - cls[:-1]) / cls[:-1]  # daily returns
    # 每日收益率

    # excess daily returns = strategy returns - financing cost, assuming a
    # risk-free rate of 4% per annum and 252 trading days in a year
    # 超额每日收益率 = 策略收益率 - 融资成本，假设年化无风险利率为 4%，
    # 一年有 252 个交易日
    excess_ret = dailyret - 0.04 / 252

    sharpe_ratio = np.sqrt(252) * excess_ret.mean() / excess_ret.std()
    # the output should be 0.7893
    # 输出结果应为 0.7893
    print("sharpeRatio = %.4f   (the book says 0.7893)" % sharpe_ratio)
    return sharpe_ratio


if __name__ == "__main__":
    main()
