"""Tests for the small helper functions of the book.
书中各种小型辅助函数的测试。
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.assert_ import assert_
from epchan.backshift import backshift
from epchan.calculate_maxdd import calculate_maxdd
from epchan.cols import cols
from epchan.fill_missing_data import fill_missing_data
from epchan.fwdshift import fwdshift
from epchan.is_last_trading_day_of_month import is_last_trading_day_of_month
from epchan.lag import lag
from epchan.lag1 import lag1
from epchan.rows import rows
from epchan.tdiff import tdiff
from epchan.trimr import trimr


class SizeTest(unittest.TestCase):
    """Tests for the ``rows`` and ``cols`` helpers.
    ``rows`` 与 ``cols`` 辅助函数的测试。
    """

    def test_rows_and_cols_of_matrix(self):
        """A matrix reports its number of rows and of columns.
        矩阵会给出它的行数与列数。
        """
        x = np.zeros((3, 4))
        self.assertEqual(rows(x), 3)
        self.assertEqual(cols(x), 4)

    def test_vector_is_a_column(self):
        """A vector is treated as a column, exactly like in MATLAB.
        向量被当作一列处理，与 MATLAB 一致。
        """
        x = np.arange(5.0)
        self.assertEqual(rows(x), 5)
        self.assertEqual(cols(x), 1)


class TrimrTest(unittest.TestCase):
    """Tests for ``trimr``, which strips rows from the top and the bottom.
    ``trimr`` 的测试，它从顶部和底部删去若干行。
    """

    def test_trims_both_ends(self):
        """The first ``n1`` and the last ``n2`` rows are removed.
        前 ``n1`` 行和后 ``n2`` 行会被去掉。
        """
        x = np.arange(10.0)
        np.testing.assert_array_equal(trimr(x, 2, 3), [2, 3, 4, 5, 6])

    def test_trims_matrix_rows(self):
        """For a matrix only the rows are trimmed, the columns stay.
        对矩阵只删行，列保持不变。
        """
        x = np.arange(12.0).reshape(4, 3)
        self.assertEqual(trimr(x, 1, 1).shape, (2, 3))

    def test_trimming_too_much_raises(self):
        """Trimming more rows than there are is an error.
        要删的行数超过实际行数时应当报错。
        """
        with self.assertRaises(ValueError):
            trimr(np.arange(5.0), 3, 2)


class LagTest(unittest.TestCase):
    """Tests for ``lag``, which shifts values forward in time.
    ``lag`` 的测试，它把数值沿时间轴向前移动。
    """

    def test_lag_pads_with_zero(self):
        """By default the padded values are zero.
        默认情况下填充值为零。
        """
        np.testing.assert_array_equal(lag(np.arange(1.0, 5.0)), [0, 1, 2, 3])

    def test_lag_with_order_and_value(self):
        """The order and the padding value can both be chosen.
        滞后的阶数与填充值都可以指定。
        """
        np.testing.assert_array_equal(lag(np.arange(1.0, 6.0), 2, -1.0),
                                      [-1, -1, 1, 2, 3])

    def test_lag_zero_order_is_empty(self):
        """A lag of order zero returns an empty array, like in MATLAB.
        阶数为 0 的滞后返回空数组，与 MATLAB 一致。
        """
        self.assertEqual(lag(np.arange(5.0), 0).size, 0)

    def test_lag_keeps_matrix_shape(self):
        """The shape of the input is preserved.
        输入的形状保持不变。
        """
        x = np.arange(6.0).reshape(3, 2)
        np.testing.assert_array_equal(lag(x, 1), [[0, 0], [0, 1], [2, 3]])


class Lag1Test(unittest.TestCase):
    """Tests for ``lag1``, the one period lag used all over the book.
    ``lag1`` 的测试，它是书中到处都在用的一期滞后。
    """

    def test_first_row_is_nan(self):
        """The first row has no predecessor and is filled with ``NaN``.
        第一行没有前值，用 ``NaN`` 填充。
        """
        y = lag1(np.array([1.0, 2.0, 3.0]))
        self.assertTrue(np.isnan(y[0]))
        np.testing.assert_array_equal(y[1:], [1.0, 2.0])

    def test_matrix(self):
        """A matrix is shifted down by one row.
        矩阵整体下移一行。
        """
        x = np.arange(6.0).reshape(3, 2)
        y = lag1(x)
        self.assertEqual(y.shape, (3, 2))
        self.assertTrue(np.isnan(y[0]).all())
        np.testing.assert_array_equal(y[1:], x[:-1])

    def test_character_array(self):
        """Character arrays are padded with an empty string.
        字符数组用空字符串填充。
        """
        y = lag1(np.array(["a", "b"]))
        self.assertEqual(y[0], "")
        self.assertEqual(y[1], "a")


class ShiftTest(unittest.TestCase):
    """Tests for ``backshift`` and ``fwdshift``.
    ``backshift`` 与 ``fwdshift`` 的测试。
    """

    def test_backshift(self):
        """``backshift`` looks into the past and pads the front with ``NaN``.
        ``backshift`` 去看过去的数据，并在前面用 ``NaN`` 填充。
        """
        np.testing.assert_array_equal(
            backshift(2, np.array([1.0, 2.0, 3.0, 4.0]))[2:], [1.0, 2.0])
        self.assertTrue(
            np.isnan(backshift(2, np.array([1.0, 2.0, 3.0, 4.0]))[:2]).all())

    def test_backshift_negative_day_raises(self):
        """A negative number of days is an error.
        天数为负时应当报错。
        """
        with self.assertRaises(ValueError):
            backshift(-1, np.arange(3.0))

    def test_fwdshift(self):
        """``fwdshift`` looks into the future and pads the back with ``NaN``.
        ``fwdshift`` 去看未来的数据，并在后面用 ``NaN`` 填充。
        """
        y = fwdshift(2, np.array([1.0, 2.0, 3.0, 4.0]))
        np.testing.assert_array_equal(y[:2], [3.0, 4.0])
        self.assertTrue(np.isnan(y[2:]).all())

    def test_fwdshift_matches_matlab_shape(self):
        """The number of rows does not change.
        行数保持不变。
        """
        x = np.arange(10.0).reshape(5, 2)
        self.assertEqual(fwdshift(2, x).shape, (5, 2))


class TdiffTest(unittest.TestCase):
    """Tests for ``tdiff``, the k period difference.
    ``tdiff``（k 期差分）的测试。
    """

    def test_order_zero_is_identity(self):
        """A difference of order zero leaves the data unchanged.
        0 阶差分不改变数据。
        """
        x = np.array([1.0, 2.0, 3.0])
        np.testing.assert_array_equal(tdiff(x, 0).ravel(), x)

    def test_first_difference(self):
        """The first difference is x(t) - x(t-1).
        一阶差分即 x(t) - x(t-1)。
        """
        np.testing.assert_array_equal(tdiff(np.array([1.0, 3.0, 6.0]), 1).ravel(),
                                      [0, 2, 3])

    def test_two_period_difference(self):
        """A two period difference is x(t) - x(t-2).
        两期差分即 x(t) - x(t-2)。
        """
        np.testing.assert_array_equal(
            tdiff(np.array([1.0, 3.0, 6.0, 10.0]), 2).ravel(), [0, 0, 5, 7])

    def test_shape_is_preserved(self):
        """The shape of the input is preserved.
        输入的形状保持不变。
        """
        x = np.arange(12.0).reshape(4, 3)
        self.assertEqual(tdiff(x, 1).shape, (4, 3))

    def test_nan_propagates(self):
        """A missing value spreads to every difference that uses it.
        缺失值会传播到所有用到它的差分上。
        """
        np.testing.assert_array_equal(tdiff(np.array([1.0, np.nan, 3.0]), 1),
                                      [0.0, np.nan, np.nan])


class FillMissingDataTest(unittest.TestCase):
    """Tests for ``fillMissingData``.
    ``fillMissingData`` 的测试。
    """

    def test_carries_the_previous_value_forward(self):
        """Missing values are replaced by the last known value.
        缺失值会被上一个已知值替换掉。
        """
        x = np.array([[1.0, 10.0], [np.nan, 20.0], [3.0, np.nan]])
        np.testing.assert_array_equal(fill_missing_data(x), [[1, 10], [1, 20], [3, 20]])

    def test_first_row_is_left_alone(self):
        """The first row has nothing to carry forward, so it stays missing.
        第一行没有可以延续的值，因此保持为缺失。
        """
        x = np.array([[np.nan, 1.0], [2.0, 3.0]])
        self.assertTrue(np.isnan(fill_missing_data(x)[0, 0]))

    def test_inf_is_treated_as_missing(self):
        """An infinite value counts as missing as well.
        无穷值同样被视为缺失值。
        """
        x = np.array([[1.0], [np.inf]])
        np.testing.assert_array_equal(fill_missing_data(x), [[1.0], [1.0]])


class MaxDrawdownTest(unittest.TestCase):
    """Tests for ``calculateMaxDD``.
    ``calculateMaxDD`` 的测试。
    """

    def test_no_drawdown(self):
        """A steadily rising equity curve has no drawdown.
        净值一路上涨的曲线没有回撤。
        """
        maxdd, maxddd = calculate_maxdd(np.array([0.1, 0.2, 0.3]))
        self.assertEqual(maxdd, 0.0)
        self.assertEqual(maxddd, 0.0)

    def test_simple_drawdown(self):
        """The drawdown is measured from the high water mark to the trough.
        回撤从高水位一直算到谷底。
        """
        cumret = np.array([0.0, 0.1, 0.0, -0.1, 0.0])
        maxdd, maxddd = calculate_maxdd(cumret)
        self.assertAlmostEqual(maxdd, 1.1 / 0.9 - 1, places=12)
        self.assertEqual(maxddd, 3)


class MonthEndTest(unittest.TestCase):
    """Tests for ``isLastTradingDayOfMonth``.
    ``isLastTradingDayOfMonth`` 的测试。
    """

    def test_flags_last_trading_day(self):
        """A trading day is flagged when the next trading day is in another month.
        当下一个交易日属于另一个月份时，该交易日会被标记出来。
        """
        tday = np.array([20070129, 20070130, 20070131, 20070201, 20070228, 20070301])
        np.testing.assert_array_equal(
            is_last_trading_day_of_month(tday),
            [False, False, True, False, True, False])

    def test_last_day_is_not_flagged(self):
        """The very last observation is not a month end, there is no next day.
        最后一个观测值不是月末，因为已经没有下一个交易日了。
        """
        tday = np.array([20070130, 20070131])
        self.assertFalse(is_last_trading_day_of_month(tday)[-1])


class AssertTest(unittest.TestCase):
    """Tests for the ``assert_`` helper.
    ``assert_`` 辅助函数的测试。
    """

    def test_raises_with_message(self):
        """A false predicate raises an error that carries the message.
        断言条件为假时抛出带消息的错误。
        """
        with self.assertRaises(AssertionError) as ctx:
            assert_(False, "boom")
        self.assertIn("assertion violated: boom", str(ctx.exception))

    def test_passes_for_true(self):
        """A true predicate returns without raising anything.
        断言条件为真时不抛出任何错误。
        """
        self.assertIsNone(assert_(True))


if __name__ == "__main__":
    unittest.main()
