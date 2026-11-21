"""Tests for the MATLAB builtins re-implemented in ``epchan.matlab_compat``."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.matlab_compat import (detrend, excel_serial_to_yyyymmdd, intersect,
                                  left_divide, matlab_round, sort_index,
                                  union, xlsread)
from epchan.paths import data_path


class DetrendTest(unittest.TestCase):
    def test_p_minus_one_is_identity(self):
        x = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        np.testing.assert_array_equal(detrend(x, -1), x)

    def test_constant_removes_column_means(self):
        x = np.array([[1.0, 10.0], [3.0, 20.0], [5.0, 30.0]])
        np.testing.assert_allclose(detrend(x, 0), [[-2.0, -10.0], [0.0, 0.0], [2.0, 10.0]])

    def test_linear_trend_is_removed(self):
        t = np.arange(10.0)
        x = np.column_stack([3.0 + 2.0 * t, -1.0 + 0.5 * t])
        np.testing.assert_allclose(detrend(x, 1), np.zeros((10, 2)), atol=1e-10)

    def test_vector_input_keeps_two_dimensions(self):
        self.assertEqual(detrend(np.arange(5.0), 0).shape, (5, 1))


class SetOperationsTest(unittest.TestCase):
    def test_intersect_returns_first_indices(self):
        a = np.array([3, 1, 2, 2, 5])
        b = np.array([2, 4, 3, 3, 1])
        common, ia, ib = intersect(a, b)
        np.testing.assert_array_equal(common, [1, 2, 3])
        np.testing.assert_array_equal(a[ia], common)
        np.testing.assert_array_equal(b[ib], common)
        # first occurrence, exactly like MATLAB
        np.testing.assert_array_equal(ia, [1, 2, 0])
        np.testing.assert_array_equal(ib, [4, 0, 2])

    def test_union_is_sorted_and_unique(self):
        np.testing.assert_array_equal(union([3, 1, 2], [2, 5]), [1, 2, 3, 5])


class SortIndexTest(unittest.TestCase):
    def test_descending_input_is_sorted(self):
        t = np.array([20070301, 20070101, 20070201])
        sorted_t, idx = sort_index(t)
        np.testing.assert_array_equal(sorted_t, [20070101, 20070201, 20070301])
        np.testing.assert_array_equal(idx, [1, 2, 0])

    def test_axis_argument(self):
        x = np.array([[3.0, 1.0], [2.0, 4.0]])
        sorted_x, idx = sort_index(x, axis=1)
        np.testing.assert_array_equal(sorted_x, [[1.0, 3.0], [2.0, 4.0]])
        np.testing.assert_array_equal(idx, [[1, 0], [0, 1]])


class ExcelTest(unittest.TestCase):
    def test_known_serial(self):
        # 2001-11-26 is the first row of IGE.xls
        self.assertEqual(excel_serial_to_yyyymmdd(37221), 20011126)

    def test_xlsread_skips_the_header(self):
        num, _txt = xlsread(data_path("IGE.xls"))
        self.assertEqual(num.shape, (1504, 7))
        self.assertEqual(int(num[0, 0]), 37221)
        self.assertTrue(np.isfinite(num[:, -1]).all())


class MatlabRoundTest(unittest.TestCase):
    def test_halves_round_away_from_zero(self):
        # MATLAB round(12.5) == 13, unlike Python's banker's rounding.
        self.assertEqual(matlab_round(12.5), 13.0)
        self.assertEqual(matlab_round(-12.5), -13.0)
        self.assertEqual(matlab_round(12.4), 12.0)
        self.assertEqual(matlab_round(0.5), 1.0)

    def test_array_input(self):
        np.testing.assert_array_equal(matlab_round(np.array([1.5, 2.5, -1.5])),
                                      [2.0, 3.0, -2.0])


class LeftDivideTest(unittest.TestCase):
    def test_least_squares_solution(self):
        a = np.array([[1.0, 0.0], [0.0, 2.0], [1.0, 1.0]])
        b = np.array([[1.0], [2.0], [2.0]])
        np.testing.assert_allclose(left_divide(a, b), [[1.0], [1.0]], atol=1e-12)


if __name__ == "__main__":
    unittest.main()
