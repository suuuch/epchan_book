"""Tests for the MATLAB builtins re-implemented in ``epchan.matlab_compat``.
``epchan.matlab_compat`` 中重新实现的 MATLAB 内置函数的测试。
"""

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
    """Tests for ``detrend``.
    ``detrend`` 的测试。
    """

    def test_p_minus_one_is_identity(self):
        """A polynomial order of -1 leaves the data untouched.
        多项式阶数为 -1 时数据保持原样。
        """
        x = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        np.testing.assert_array_equal(detrend(x, -1), x)

    def test_constant_removes_column_means(self):
        """Order 0 removes the mean of every column.
        0 阶去趋势会减去每一列的均值。
        """
        x = np.array([[1.0, 10.0], [3.0, 20.0], [5.0, 30.0]])
        np.testing.assert_allclose(detrend(x, 0),
                                   [[-2.0, -10.0], [0.0, 0.0], [2.0, 10.0]])

    def test_linear_trend_is_removed(self):
        """Order 1 removes a linear trend from every column.
        1 阶去趋势会去掉每一列的线性趋势。
        """
        t = np.arange(10.0)
        x = np.column_stack([3.0 + 2.0 * t, -1.0 + 0.5 * t])
        np.testing.assert_allclose(detrend(x, 1), np.zeros((10, 2)), atol=1e-10)

    def test_vector_input_keeps_two_dimensions(self):
        """A vector is treated as a single column.
        向量被当作单独一列处理。
        """
        self.assertEqual(detrend(np.arange(5.0), 0).shape, (5, 1))


class SetOperationsTest(unittest.TestCase):
    """Tests for ``intersect`` and ``union``.
    ``intersect`` 与 ``union`` 的测试。
    """

    def test_intersect_returns_first_indices(self):
        """The indices point at the first occurrence, exactly like MATLAB.
        索引指向首次出现的位置，与 MATLAB 完全一致。
        """
        a = np.array([3, 1, 2, 2, 5])
        b = np.array([2, 4, 3, 3, 1])
        common, ia, ib = intersect(a, b)
        np.testing.assert_array_equal(common, [1, 2, 3])
        np.testing.assert_array_equal(a[ia], common)
        np.testing.assert_array_equal(b[ib], common)
        # first occurrence, exactly like MATLAB
        # 首次出现的位置，与 MATLAB 完全一致
        np.testing.assert_array_equal(ia, [1, 2, 0])
        np.testing.assert_array_equal(ib, [4, 0, 2])

    def test_union_is_sorted_and_unique(self):
        """The union is sorted and free of duplicates.
        并集是排序过的，并且没有重复元素。
        """
        np.testing.assert_array_equal(union([3, 1, 2], [2, 5]), [1, 2, 3, 5])


class SortIndexTest(unittest.TestCase):
    """Tests for ``sort_index``.
    ``sort_index`` 的测试。
    """

    def test_descending_input_is_sorted(self):
        """The values are sorted in ascending order together with their indices.
        数值按升序排列，并同时给出对应的索引。
        """
        t = np.array([20070301, 20070101, 20070201])
        sorted_t, idx = sort_index(t)
        np.testing.assert_array_equal(sorted_t, [20070101, 20070201, 20070301])
        np.testing.assert_array_equal(idx, [1, 2, 0])

    def test_axis_argument(self):
        """The sorting can be done along the rows or along the columns.
        排序既可以沿行进行，也可以沿列进行。
        """
        x = np.array([[3.0, 1.0], [2.0, 4.0]])
        sorted_x, idx = sort_index(x, axis=1)
        np.testing.assert_array_equal(sorted_x, [[1.0, 3.0], [2.0, 4.0]])
        np.testing.assert_array_equal(idx, [[1, 0], [0, 1]])


class ExcelTest(unittest.TestCase):
    """Tests for the Excel spreadsheet readers.
    Excel 电子表格读取函数的测试。
    """

    def test_known_serial(self):
        """The Excel serial number of a known date is converted correctly.
        已知日期对应的 Excel 序列号被正确转换。
        """
        # 2001-11-26 is the first row of IGE.xls
        # 2001-11-26 是 IGE.xls 的第一行
        self.assertEqual(excel_serial_to_yyyymmdd(37221), 20011126)

    def test_xlsread_skips_the_header(self):
        """The header row is not returned as data.
        表头行不会作为数据返回。
        """
        num, _txt = xlsread(data_path("IGE.xls"))
        self.assertEqual(num.shape, (1504, 7))
        self.assertEqual(int(num[0, 0]), 37221)
        self.assertTrue(np.isfinite(num[:, -1]).all())


class MatlabRoundTest(unittest.TestCase):
    """Tests for ``matlab_round``.
    ``matlab_round`` 的测试。
    """

    def test_halves_round_away_from_zero(self):
        """MATLAB rounds halves away from zero, unlike Python's banker's rounding.
        MATLAB 把一半取整到远离零的一侧，与 Python 的银行家舍入不同。
        """
        # MATLAB round(12.5) == 13, unlike Python's banker's rounding.
        # MATLAB 中 round(12.5) 等于 13，与 Python 的银行家舍入不同。
        self.assertEqual(matlab_round(12.5), 13.0)
        self.assertEqual(matlab_round(-12.5), -13.0)
        self.assertEqual(matlab_round(12.4), 12.0)
        self.assertEqual(matlab_round(0.5), 1.0)

    def test_array_input(self):
        """The rounding works element wise on arrays.
        该函数可以逐元素地作用于数组。
        """
        np.testing.assert_array_equal(matlab_round(np.array([1.5, 2.5, -1.5])),
                                      [2.0, 3.0, -2.0])


class LeftDivideTest(unittest.TestCase):
    """Tests for ``left_divide``, the least squares solution of ``A \\ b``.
    ``left_divide``（即 ``A \\ b`` 的最小二乘解）的测试。
    """

    def test_least_squares_solution(self):
        """The solution minimises the sum of squared errors.
        该解使误差平方和最小。
        """
        a = np.array([[1.0, 0.0], [0.0, 2.0], [1.0, 1.0]])
        b = np.array([[1.0], [2.0], [2.0]])
        np.testing.assert_allclose(left_divide(a, b), [[1.0], [1.0]], atol=1e-12)


if __name__ == "__main__":
    unittest.main()
