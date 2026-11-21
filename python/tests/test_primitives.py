"""Tests for the small helper functions of the book."""

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
    def test_rows_and_cols_of_matrix(self):
        x = np.zeros((3, 4))
        self.assertEqual(rows(x), 3)
        self.assertEqual(cols(x), 4)

    def test_vector_is_a_column(self):
        x = np.arange(5.0)
        self.assertEqual(rows(x), 5)
        self.assertEqual(cols(x), 1)


class TrimrTest(unittest.TestCase):
    def test_trims_both_ends(self):
        x = np.arange(10.0)
        np.testing.assert_array_equal(trimr(x, 2, 3), [2, 3, 4, 5, 6])

    def test_trims_matrix_rows(self):
        x = np.arange(12.0).reshape(4, 3)
        self.assertEqual(trimr(x, 1, 1).shape, (2, 3))

    def test_trimming_too_much_raises(self):
        with self.assertRaises(ValueError):
            trimr(np.arange(5.0), 3, 2)


class LagTest(unittest.TestCase):
    def test_lag_pads_with_zero(self):
        np.testing.assert_array_equal(lag(np.arange(1.0, 5.0)), [0, 1, 2, 3])

    def test_lag_with_order_and_value(self):
        np.testing.assert_array_equal(lag(np.arange(1.0, 6.0), 2, -1.0), [-1, -1, 1, 2, 3])

    def test_lag_zero_order_is_empty(self):
        self.assertEqual(lag(np.arange(5.0), 0).size, 0)

    def test_lag_keeps_matrix_shape(self):
        x = np.arange(6.0).reshape(3, 2)
        np.testing.assert_array_equal(lag(x, 1), [[0, 0], [0, 1], [2, 3]])


class Lag1Test(unittest.TestCase):
    def test_first_row_is_nan(self):
        y = lag1(np.array([1.0, 2.0, 3.0]))
        self.assertTrue(np.isnan(y[0]))
        np.testing.assert_array_equal(y[1:], [1.0, 2.0])

    def test_matrix(self):
        x = np.arange(6.0).reshape(3, 2)
        y = lag1(x)
        self.assertEqual(y.shape, (3, 2))
        self.assertTrue(np.isnan(y[0]).all())
        np.testing.assert_array_equal(y[1:], x[:-1])

    def test_character_array(self):
        y = lag1(np.array(["a", "b"]))
        self.assertEqual(y[0], "")
        self.assertEqual(y[1], "a")


class ShiftTest(unittest.TestCase):
    def test_backshift(self):
        np.testing.assert_array_equal(backshift(2, np.array([1.0, 2.0, 3.0, 4.0]))[2:], [1.0, 2.0])
        self.assertTrue(np.isnan(backshift(2, np.array([1.0, 2.0, 3.0, 4.0]))[:2]).all())

    def test_backshift_negative_day_raises(self):
        with self.assertRaises(ValueError):
            backshift(-1, np.arange(3.0))

    def test_fwdshift(self):
        y = fwdshift(2, np.array([1.0, 2.0, 3.0, 4.0]))
        np.testing.assert_array_equal(y[:2], [3.0, 4.0])
        self.assertTrue(np.isnan(y[2:]).all())

    def test_fwdshift_matches_matlab_shape(self):
        x = np.arange(10.0).reshape(5, 2)
        self.assertEqual(fwdshift(2, x).shape, (5, 2))


class TdiffTest(unittest.TestCase):
    def test_order_zero_is_identity(self):
        x = np.array([1.0, 2.0, 3.0])
        np.testing.assert_array_equal(tdiff(x, 0).ravel(), x)

    def test_first_difference(self):
        np.testing.assert_array_equal(tdiff(np.array([1.0, 3.0, 6.0]), 1).ravel(), [0, 2, 3])

    def test_two_period_difference(self):
        np.testing.assert_array_equal(
            tdiff(np.array([1.0, 3.0, 6.0, 10.0]), 2).ravel(), [0, 0, 5, 7])

    def test_shape_is_preserved(self):
        x = np.arange(12.0).reshape(4, 3)
        self.assertEqual(tdiff(x, 1).shape, (4, 3))

    def test_nan_propagates(self):
        np.testing.assert_array_equal(tdiff(np.array([1.0, np.nan, 3.0]), 1),
                                      [0.0, np.nan, np.nan])


class FillMissingDataTest(unittest.TestCase):
    def test_carries_the_previous_value_forward(self):
        x = np.array([[1.0, 10.0], [np.nan, 20.0], [3.0, np.nan]])
        np.testing.assert_array_equal(fill_missing_data(x), [[1, 10], [1, 20], [3, 20]])

    def test_first_row_is_left_alone(self):
        x = np.array([[np.nan, 1.0], [2.0, 3.0]])
        self.assertTrue(np.isnan(fill_missing_data(x)[0, 0]))

    def test_inf_is_treated_as_missing(self):
        x = np.array([[1.0], [np.inf]])
        np.testing.assert_array_equal(fill_missing_data(x), [[1.0], [1.0]])


class MaxDrawdownTest(unittest.TestCase):
    def test_no_drawdown(self):
        maxdd, maxddd = calculate_maxdd(np.array([0.1, 0.2, 0.3]))
        self.assertEqual(maxdd, 0.0)
        self.assertEqual(maxddd, 0.0)

    def test_simple_drawdown(self):
        cumret = np.array([0.0, 0.1, 0.0, -0.1, 0.0])
        maxdd, maxddd = calculate_maxdd(cumret)
        self.assertAlmostEqual(maxdd, 1.1 / 0.9 - 1, places=12)
        self.assertEqual(maxddd, 3)


class MonthEndTest(unittest.TestCase):
    def test_flags_last_trading_day(self):
        tday = np.array([20070129, 20070130, 20070131, 20070201, 20070228, 20070301])
        np.testing.assert_array_equal(
            is_last_trading_day_of_month(tday),
            [False, False, True, False, True, False])

    def test_last_day_is_not_flagged(self):
        tday = np.array([20070130, 20070131])
        self.assertFalse(is_last_trading_day_of_month(tday)[-1])


class AssertTest(unittest.TestCase):
    def test_raises_with_message(self):
        with self.assertRaises(AssertionError) as ctx:
            assert_(False, "boom")
        self.assertIn("assertion violated: boom", str(ctx.exception))

    def test_passes_for_true(self):
        self.assertIsNone(assert_(True))


if __name__ == "__main__":
    unittest.main()
