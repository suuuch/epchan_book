"""Tests for the ``smart*`` statistics and the data readers.
``smart*`` 系列统计函数以及数据读取函数的测试。

In this port MATLAB's ``dim`` argument becomes the 0-based numpy ``axis``
(MATLAB ``dim=1`` is numpy ``axis=0``).

在本移植版本中，MATLAB 的 ``dim`` 参数对应 numpy 的 0 起始 ``axis``
（MATLAB 的 ``dim=1`` 即 numpy 的 ``axis=0``）。
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.get_cls import get_cls
from epchan.get_tday import get_tday
from epchan.paths import data_path
from epchan.smartcov import smartcov
from epchan.smartmean import smartmean
from epchan.smartmean1 import smartmean1
from epchan.smartstd import smartstd
from epchan.smartstd1 import smartstd1
from epchan.smartsum import smartsum


class SmartMeanTest(unittest.TestCase):
    """Tests for ``smartmean`` and ``smartmean1``.
    ``smartmean`` 与 ``smartmean1`` 的测试。
    """

    def setUp(self):
        """Build a small matrix holding a NaN and an infinite value.
        构造一个含有 NaN 和无穷值的小矩阵。
        """
        self.x = np.array([[1.0, np.nan], [3.0, np.inf], [5.0, 6.0]])

    def test_mean_along_columns_ignores_missing(self):
        """Missing values are skipped, so the column means use what is left.
        缺失值会被跳过，因此列均值只由其余观测值算出。
        """
        np.testing.assert_allclose(smartmean(self.x, axis=0), [3.0, 6.0])

    def test_mean_along_rows(self):
        """The row mean of a row containing a NaN uses the remaining values.
        含 NaN 那一行的行均值只由该行其余的值算出。
        """
        np.testing.assert_allclose(smartmean(self.x, axis=1), [1.0, 3.0, 5.5])

    def test_all_missing_slice_is_nan(self):
        """A slice without any usable observation has a NaN mean.
        完全没有可用观测值的切片，其均值为 NaN。
        """
        y = smartmean(np.full((2, 2), np.nan), axis=0)
        self.assertTrue(np.isnan(y).all())

    def test_default_axis_is_first_non_singleton(self):
        """Without an axis the first non-singleton dimension is used.
        不给 axis 时，使用第一个长度不为 1 的维度。
        """
        self.assertAlmostEqual(smartmean(np.array([1.0, 2.0, 3.0])), 2.0)
        np.testing.assert_allclose(smartmean(self.x), [3.0, 6.0])

    def test_smartmean1_matches_smartmean(self):
        """``smartmean1`` is the older, row-wise variant of ``smartmean``.
        ``smartmean1`` 是 ``smartmean`` 的旧版（逐行）变体。
        """
        np.testing.assert_allclose(smartmean1(self.x, 0), smartmean(self.x, 0))


class SmartSumTest(unittest.TestCase):
    """Tests for ``smartsum``.
    ``smartsum`` 的测试。
    """

    def test_sum_ignores_missing(self):
        """Missing values are skipped when summing a column.
        沿列求和时缺失值会被跳过。
        """
        x = np.array([[1.0, np.nan], [3.0, 4.0]])
        np.testing.assert_allclose(smartsum(x, axis=0), [4.0, 4.0])

    def test_all_missing_slice_is_nan(self):
        """A slice without any usable observation has a NaN sum.
        完全没有可用观测值的切片，其和为 NaN。
        """
        x = np.array([[np.nan], [np.nan]])
        self.assertTrue(np.isnan(smartsum(x, axis=0)).all())

    def test_sums_rows(self):
        """Summing along the rows skips the missing entry.
        沿行求和时会跳过缺失的那一项。
        """
        np.testing.assert_allclose(smartsum(np.array([[1.0, 2.0], [3.0, np.nan]]), 1),
                                   [3.0, 3.0])


class SmartStdTest(unittest.TestCase):
    """Tests for ``smartstd`` and ``smartstd1``.
    ``smartstd`` 与 ``smartstd1`` 的测试。
    """

    def test_normalised_by_n(self):
        """``smartstd`` divides by n, ``smartstd1`` by n-1, as in MATLAB.
        与 MATLAB 一样，``smartstd`` 除以 n，``smartstd1`` 除以 n-1。
        """
        x = np.array([[1.0], [3.0]])
        self.assertAlmostEqual(smartstd(x, 0)[0], 1.0)  # population std
        # 总体标准差
        self.assertAlmostEqual(smartstd1(x, 0)[0], np.sqrt(2.0))  # sample std
        # 样本标准差

    def test_ignores_missing(self):
        """Missing values are skipped, a column with one value has std zero.
        缺失值会被跳过，只有一个有效值的列其标准差为零。
        """
        x = np.array([[1.0, np.nan], [3.0, np.nan], [5.0, 9.0]])
        np.testing.assert_allclose(smartstd(x, 0), [np.sqrt(8.0 / 3.0), 0.0])

    def test_all_missing_is_nan(self):
        """A column without any usable observation has a NaN standard deviation.
        没有任何可用观测值的列，其标准差为 NaN。
        """
        self.assertTrue(np.isnan(smartstd(np.full((3, 1), np.nan), 0)).all())
        self.assertTrue(np.isnan(smartstd1(np.full((3, 1), np.nan), 0)).all())


class SmartCovTest(unittest.TestCase):
    """Tests for ``smartcov``.
    ``smartcov`` 的测试。
    """

    def test_matches_matlab_algorithm(self):
        """The result equals the double loop of the original MATLAB code.
        结果应与原始 MATLAB 代码中的双重循环一致。
        """
        rng = np.random.default_rng(1)
        x = rng.normal(size=(30, 3))
        x[2, 1] = np.nan
        x[5, 2] = np.nan

        # Direct transcription of the MATLAB double loop.
        # MATLAB 双重循环的直接翻译。
        expected = np.full((3, 3), np.nan)
        xc = x - smartmean(x, axis=0)
        for m in range(3):
            for n in range(m, 3):
                expected[m, n] = smartmean(xc[:, m] * xc[:, n], axis=0)
                expected[n, m] = expected[m, n]

        np.testing.assert_allclose(smartcov(x), expected, equal_nan=True)

    def test_entirely_nan_column_stays_nan(self):
        """A column without any usable observation keeps the whole row/column NaN.
        没有任何可用观测值的列，其整行整列都保持为 NaN。
        """
        x = np.array([[1.0, np.nan], [2.0, np.nan], [3.0, np.nan]])
        cov = smartcov(x)
        self.assertTrue(np.isnan(cov[1, :]).all())
        self.assertTrue(np.isnan(cov[:, 1]).all())
        self.assertAlmostEqual(cov[0, 0], 2.0 / 3.0)


class ReaderTest(unittest.TestCase):
    """Tests for the ``getTday`` and ``getCls`` data readers.
    ``getTday`` 与 ``getCls`` 数据读取函数的测试。
    """

    def test_get_tday_returns_dates_and_prices(self):
        """The reader returns one adjusted close price per trading day.
        读取函数为每个交易日返回一条复权收盘价。
        """
        tday, adjcls = get_tday(data_path("IGE.xls"))
        self.assertEqual(len(tday), 1504)
        self.assertEqual(len(adjcls), 1504)
        self.assertEqual(min(tday), 20011126)
        self.assertEqual(max(tday), 20071114)

    def test_get_cls_sorts_by_date(self):
        """``getCls`` returns the prices in ascending date order.
        ``getCls`` 按日期升序返回价格。
        """
        cls = get_cls(data_path("IGE.xls"))
        tday, raw = get_tday(data_path("IGE.xls"))
        self.assertEqual(len(cls), len(raw))
        # the prices must follow the ascending date order
        # 价格必须按日期升序排列
        np.testing.assert_array_equal(cls, raw[np.argsort(tday, kind="stable")])


if __name__ == "__main__":
    unittest.main()
