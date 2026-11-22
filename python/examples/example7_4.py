"""Port of ``example7_4.m``: a factor model based momentum strategy.

The book says the annualised average return of the trading strategy is a very
poor -1.8099.
书中给出的交易策略年化平均收益率非常差，为 -1.8099。
"""

import sys
from pathlib import Path

# Add this folder to the Python path, just like the MATLAB original adds this
# folder and the data folder to the MATLAB path.
# 将本文件夹添加到 Python 路径中，就像 MATLAB 原版把本文件夹和数据文件夹
# 添加到 MATLAB 路径中那样。
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from scipy.io import loadmat

from epchan.backshift import backshift
from epchan.fill_missing_data import fill_missing_data
from epchan.lag1 import lag1
from epchan.ols import ols
from epchan.paths import data_path
from epchan.smartcov import smartcov
from epchan.smartmean import smartmean
from epchan.smartsum import smartsum


def main():
    lookback = 252  # use lookback days as estimation (training) period
    # 使用 lookback 天作为估计（训练）期，以确定因子暴露。
    num_factors = 5
    topn = 50  # long stocks with topN expected 1-day returns
    # 对于交易策略，做多预期 1 日收益率最高的 topN 只股票。

    # test on SP600 smallcap stocks.
    # 在 SP600 小盘股上测试。
    # (This MATLAB binary input file contains tday, stocks, op, hi, lo, cl arrays.
    # 该 MATLAB 二进制输入文件包含 tday、stocks、op、hi、lo、cl 数组。
    # save('myfile.mat','-v6');
    # 保存数据: save('myfile.mat','-v6');
    mat = loadmat(data_path("IJR_20080114.mat"))
    tday = mat["tday"].ravel()
    cl = mat["cl"]

    mycls = fill_missing_data(cl)

    positions_table = np.zeros_like(cl)

    # note the rows of dailyret are the observations at different time periods
    # 注意 dailyret 的行对应不同时期的观测值
    dailyret = (mycls - lag1(mycls)) / lag1(mycls)

    # ``i`` is the 0-based row of day ``t`` of the MATLAB loop
    # ``for t=lookback+1:length(tday)``.
    # ``i`` 对应 MATLAB 循环 ``for t=lookback+1:length(tday)`` 中第 ``t`` 天的
    # 从 0 开始计的行号。
    for i in range(lookback, len(tday)):
        # here the columns of R are the different observations.
        # 此处 R 的列对应不同的观测值。
        R = dailyret[i - lookback + 1:i + 1, :].T

        # avoid stocks with missing returns
        # 剔除收益率有缺失的股票
        has_data = np.flatnonzero(np.all(np.isfinite(R), axis=1))

        R = R[has_data, :]

        # ``avg_r`` is a column vector, as in MATLAB's ``smartmean(R, 2)``.
        # ``avg_r`` 是列向量，与 MATLAB 的 ``smartmean(R, 2)`` 一致。
        avg_r = smartmean(R, axis=1).reshape(-1, 1)
        R = R - avg_r  # subtract mean from returns
        # 从收益率中减去均值

        cov_r = smartcov(R.T)  # compute covariance matrix, with observations in rows.
        # 计算协方差矩阵，观测值按行排列。

        # X is the factor exposures matrix, B the variances of factor returns.
        # MATLAB's eig() returns the eigenvalues in ascending order; numpy's
        # eigh() does the same but returns them *before* the eigenvectors.
        # X 是因子暴露矩阵，B 是因子收益率的方差。
        # MATLAB 的 eig() 按升序返回特征值；numpy 的 eigh() 顺序相同，但把特征值
        # 放在特征向量*之前*返回。
        _B, X = np.linalg.eigh(cov_r)

        X = X[:, X.shape[1] - num_factors:]  # Retain only numFactors
        # 只保留 numFactors

        # b are the factor returns for time period t-1 to t.
        # b 是 t-1 到 t 期的因子收益率。
        results = ols(R[:, -1], X)
        b = results.beta

        # Rexp is the expected return for next period assuming factor returns
        # remain constant.
        # Rexp 是假设因子收益率保持不变时下一期的预期收益率。
        rexp = (avg_r + X @ b).ravel()

        idx_sort = np.argsort(rexp, kind="stable")

        # short topN stocks with lowest expected returns
        # 做空预期收益率最低的 topN 只股票
        positions_table[i, has_data[idx_sort[:topn]]] = -1
        # buy topN stocks with highest expected returns
        # 买入预期收益率最高的 topN 只股票
        # has_data[idx_sort[-topn:]] = 1
        # 设置持仓为 1: has_data[idx_sort[-topn:]] = 1;
        positions_table[i, has_data[idx_sort[-topn:]]] = 1

    # compute daily returns of trading strategy
    # 计算交易策略的每日收益率
    ret = smartsum(backshift(1, positions_table) * dailyret, axis=1)
    # compute annualized average return of trading strategy
    # 计算交易策略的年化平均收益率
    avgret = smartmean(ret) * 252
    # A very poor return!
    # 非常差的收益率！
    # avgret =
    #
    #    -1.8099
    print("avgret = %.4f   (the book says -1.8099)" % avgret)
    return avgret


if __name__ == "__main__":
    main()
