"""Tests for ``ols``, ``cadf``, ``rztcrit`` and the printing helpers.
``ols``、``cadf``、``rztcrit`` 以及打印辅助函数的测试。
"""

import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from epchan.cadf import cadf
from epchan.get_tday import get_tday
from epchan.matlab_compat import intersect, union
from epchan.mprint import mprint
from epchan.ols import ols
from epchan.paths import data_path
from epchan.prt import prt
from epchan.rztcrit import rztcrit


class OlsTest(unittest.TestCase):
    """Tests for the ordinary least squares routine.
    普通最小二乘回归的测试。
    """

    def test_exact_fit(self):
        """A perfectly linear relationship is fitted with zero residual.
        完全线性的关系应当被精确拟合，残差为零。
        """
        x = np.column_stack([np.ones(20), np.arange(20.0)])
        y = 3.0 + 2.0 * x[:, 1]
        res = ols(y, x)
        np.testing.assert_allclose(res.beta.ravel(), [3.0, 2.0], atol=1e-10)
        self.assertAlmostEqual(res.rsqr, 1.0)
        self.assertEqual(res.nobs, 20)
        self.assertEqual(res.nvar, 2)

    def test_against_numpy_lstsq(self):
        """The coefficients agree with numpy's least squares solver.
        回归系数应与 numpy 的最小二乘求解结果一致。
        """
        rng = np.random.default_rng(7)
        x = np.column_stack([np.ones(50), rng.normal(size=(50, 3))])
        y = rng.normal(size=50)
        res = ols(y, x)
        expected, *_ = np.linalg.lstsq(x, y, rcond=None)
        np.testing.assert_allclose(res.beta.ravel(), expected, atol=1e-10)

    def test_tstatistics_match_scipy(self):
        """The t-statistics and the confidence intervals are consistent.
        t 统计量与置信区间应当彼此一致。
        """
        rng = np.random.default_rng(11)
        x = np.column_stack([np.ones(100), rng.normal(size=(100, 2))])
        y = x @ np.array([1.0, 2.0, -1.0]) + rng.normal(size=100)
        res = ols(y, x)
        # recompute the standard errors independently
        # 独立地重新计算标准误
        resid = y - x @ res.beta.ravel()
        s2 = resid @ resid / (100 - 3)
        cov = s2 * np.linalg.inv(x.T @ x)
        np.testing.assert_allclose(res.tstat.ravel(),
                                   res.beta.ravel() / np.sqrt(np.diag(cov)), rtol=1e-8)
        np.testing.assert_allclose(
            res.bint[:, 0], res.beta.ravel() - 1.96 * np.sqrt(np.diag(cov)),
            rtol=1e-2)

    def test_mismatched_lengths_raise(self):
        """A different number of observations in ``y`` and ``x`` is an error.
        ``y`` 与 ``x`` 的观测值个数不一致时应当报错。
        """
        with self.assertRaises(ValueError):
            ols(np.zeros(3), np.zeros((4, 1)))


class RztcritTest(unittest.TestCase):
    """Tests for the critical value tables of the augmented DF test.
    增广 DF 检验临界值表的测试。
    """

    def test_book_values_for_gld_gdx(self):
        """The book's example7_2 prints -3.819 / -3.343 / -3.042.
        书中的例 7_2 打印出 -3.819 / -3.343 / -3.042。
        """
        # The book's example7_2 prints -3.819 / -3.343 / -3.042.
        # 书中的例 7_2 打印出 -3.819 / -3.343 / -3.042。
        crit = rztcrit(450, 1, 0).ravel()
        np.testing.assert_allclose(crit[:3], [-3.81898, -3.34274, -3.04197])

    def test_small_sample_bracket(self):
        """With fewer than 200 observations a different table is used.
        观测值少于 200 时会改用另一张表。
        """
        np.testing.assert_allclose(rztcrit(100, 1, 0).ravel()[:3],
                                   [-4.02456, -3.40397, -3.08903])

    def test_unknown_combination_raises(self):
        """A combination that is not in the tables is an error.
        表中不存在的组合应当报错。
        """
        with self.assertRaises(ValueError):
            rztcrit(450, 9, 0)


class CadfTest(unittest.TestCase):
    """Tests for the cointegration test on the book's KO/PEP data.
    用书中的 KO/PEP 数据做协整检验的测试。
    """

    @classmethod
    def setUpClass(cls):
        """Run the cointegration test once for the whole test class.
        为整个测试类统一跑一次协整检验。
        """
        tday1, adjcls1 = get_tday(data_path("KO.xls"))
        tday2, adjcls2 = get_tday(data_path("PEP.xls"))
        tday = union(tday1, tday2)
        _c, idx, idx1 = intersect(tday, tday1)
        adjcls = np.full((len(tday), 2), np.nan)
        adjcls[idx, 0] = adjcls1[idx1]
        _c, idx, idx2 = intersect(tday, tday2)
        adjcls[idx, 1] = adjcls2[idx2]
        baddata = np.flatnonzero(~np.isfinite(adjcls).all(axis=1))
        adjcls = np.delete(adjcls, baddata, axis=0)
        cls.res = cadf(adjcls[:, 0], adjcls[:, 1], 0, 1)

    def test_the_book_numbers(self):
        """The test statistic is the one printed in example 7.3 of the book.
        检验统计量应与书中例 7.3 打印的一致。
        """
        self.assertAlmostEqual(self.res.adf, -2.14258438, places=7)
        self.assertAlmostEqual(self.res.alpha, -0.001167, places=5)
        self.assertEqual(self.res.nlag, 1)
        self.assertEqual(self.res.nvar, 1)
        self.assertEqual(self.res.meth, "cadf")

    def test_critical_values(self):
        """The critical values attached to the statistic are the book's ones.
        与统计量一起给出的临界值应与书中一致。
        """
        np.testing.assert_allclose(self.res.crit.ravel()[:3],
                                   [-3.880, -3.359, -3.038], atol=1e-3)


class PrintingTest(unittest.TestCase):
    """Tests for the ``mprint`` and ``prt`` output helpers.
    ``mprint`` 与 ``prt`` 输出辅助函数的测试。
    """

    def test_mprint_formats_numbers(self):
        """The numbers are printed with the requested format.
        数字应按请求的格式打印。
        """
        out = io.StringIO()
        mprint(np.array([[1.5, 2.0]]), {"fmt": "%8.2f", "fid": out})
        self.assertIn("1.50", out.getvalue())
        self.assertIn("2.00", out.getvalue())

    def test_mprint_accepts_missing_percent(self):
        """A format without the percent sign is treated like MATLAB's.
        缺少百分号的格式串按 MATLAB 的方式处理。
        """
        out = io.StringIO()
        mprint(np.array([[1.23456789]]), {"fmt": "16.6f", "fid": out})
        self.assertIn("1.234568", out.getvalue())

    def test_mprint_writes_column_names(self):
        """The column names are printed above the numbers.
        列名会打印在数字的上方。
        """
        out = io.StringIO()
        mprint(np.array([[1.0, 2.0]]), {"cnames": ["a", "b"], "fid": out})
        self.assertIn("a", out.getvalue())
        self.assertIn("b", out.getvalue())

    def test_prt_prints_cointegration_results(self):
        """``prt`` prints the augmented DF table for a pair of series.
        ``prt`` 会为一对序列打印增广 DF 检验表格。
        """
        tday1, adjcls1 = get_tday(data_path("KO.xls"))
        tday2, adjcls2 = get_tday(data_path("PEP.xls"))
        tday = union(tday1, tday2)
        _c, idx, idx1 = intersect(tday, tday1)
        adjcls = np.full((len(tday), 2), np.nan)
        adjcls[idx, 0] = adjcls1[idx1]
        _c, idx, idx2 = intersect(tday, tday2)
        adjcls[idx, 1] = adjcls2[idx2]
        adjcls = adjcls[np.isfinite(adjcls).all(axis=1)]

        out = io.StringIO()
        prt(cadf(adjcls[:, 0], adjcls[:, 1], 0, 1), ["KO", "PEP"], out)
        text = out.getvalue()
        self.assertIn("Augmented DF test for co-integration", text)
        self.assertIn("CADF t-statistic", text)
        self.assertIn("-2.14258438", text)

    def test_prt_prints_regression_results(self):
        """``prt`` prints the regression table for an ``ols`` result.
        ``prt`` 会为 ``ols`` 的结果打印回归表格。
        """
        x = np.column_stack([np.ones(10), np.arange(10.0)])
        out = io.StringIO()
        prt(ols(np.arange(10.0), x), ["const", "x1"], out)
        self.assertIn("Coefficient", out.getvalue())
        self.assertIn("R-squared", out.getvalue())

    def test_mprint_reproduces_the_book_layout(self):
        """The layout is the CADF table printed by the book for KO/PEP (example7_3).
        版式与书中例 7_3 为 KO/PEP 打印的 CADF 表格一致。
        """
        # This is the CADF table printed by the book for KO/PEP (example7_3).
        # 这就是书中例 7_3 为 KO/PEP 打印的 CADF 表格。
        out = io.StringIO()
        mprint(np.array([[-2.14258438, 1, -0.001167]]),
               {"cnames": ["CADF t-statistic", "# of lags", "AR(1) estimate"],
                "fmt": ["%16.8f", "%10d", "%16.6f"],
                "fid": out})
        lines = out.getvalue().splitlines()
        self.assertEqual(lines[0],
                         "CADF t-statistic        # of lags   AR(1) estimate ")
        self.assertEqual(lines[1],
                         "     -2.14258438          1        -0.001167 ")
        self.assertEqual(lines[2], "")

    def test_mprint_row_labels_and_formats(self):
        """The row labels and the row formats are honoured.
        行标签与行格式都会被正确处理。
        """
        out = io.StringIO()
        mprint(np.array([[1.0, 2.0], [3.0, 4.0]]),
               {"cnames": ["a", "b"], "rnames": ["row", "r1", "r2"],
                "fmt": "%6.2f", "fid": out})
        text = out.getvalue()
        self.assertIn("row", text)
        self.assertIn("r1", text)
        self.assertIn("r2", text)
        self.assertIn("  1.00", text)

    def test_mprint_rejects_wrong_number_of_formats(self):
        """One format per column is required.
        每个列必须配一个格式串。
        """
        with self.assertRaises(ValueError):
            mprint(np.zeros((2, 3)), {"fmt": ["%5.1f", "%5.1f"],
                                      "fid": io.StringIO()})

    def test_prt_johansen(self):
        """``prt`` also knows how to print a Johansen result.
        ``prt`` 也能打印 Johansen 检验的结果。
        """
        # A minimal stand-in for the structure returned by the Johansen code.
        # 充当 Johansen 代码所返回结构体的最小替身。
        class Johansen:
            meth = "johansen"
            eig = np.array([0.1, 0.2])
            ind = np.array([1, 2])
            lr1 = np.array([[30.0], [12.0]])
            cvt = np.array([[20.0, 22.0, 25.0], [9.0, 10.0, 12.0]])
            lr2 = np.array([[18.0], [7.0]])
            cvm = np.array([[15.0, 17.0, 20.0], [6.0, 7.0, 9.0]])

        out = io.StringIO()
        prt(Johansen(), ["y", "x"], out)
        text = out.getvalue()
        self.assertIn("Johansen MLE estimates", text)
        self.assertIn("Trace Statistic", text)
        self.assertIn("Eigen Statistic", text)
        self.assertIn("30.000", text)

    def test_prt_rejects_unknown_method(self):
        """A result whose method is unknown cannot be printed.
        估计方法未知的结构体无法打印。
        """
        # A result with a method that ``prt`` does not know about.
        # 估计方法是 ``prt`` 不认识的结构体。
        class Dummy:
            meth = "nope"

        with self.assertRaises(ValueError):
            prt(Dummy(), fid=io.StringIO())


if __name__ == "__main__":
    unittest.main()
