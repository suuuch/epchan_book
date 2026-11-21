"""Tests for ``ols``, ``cadf``, ``rztcrit`` and the printing helpers."""

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
    def test_exact_fit(self):
        x = np.column_stack([np.ones(20), np.arange(20.0)])
        y = 3.0 + 2.0 * x[:, 1]
        res = ols(y, x)
        np.testing.assert_allclose(res.beta.ravel(), [3.0, 2.0], atol=1e-10)
        self.assertAlmostEqual(res.rsqr, 1.0)
        self.assertEqual(res.nobs, 20)
        self.assertEqual(res.nvar, 2)

    def test_against_numpy_lstsq(self):
        rng = np.random.default_rng(7)
        x = np.column_stack([np.ones(50), rng.normal(size=(50, 3))])
        y = rng.normal(size=50)
        res = ols(y, x)
        expected, *_ = np.linalg.lstsq(x, y, rcond=None)
        np.testing.assert_allclose(res.beta.ravel(), expected, atol=1e-10)

    def test_tstatistics_match_scipy(self):
        rng = np.random.default_rng(11)
        x = np.column_stack([np.ones(100), rng.normal(size=(100, 2))])
        y = x @ np.array([1.0, 2.0, -1.0]) + rng.normal(size=100)
        res = ols(y, x)
        # recompute the standard errors independently
        resid = y - x @ res.beta.ravel()
        s2 = resid @ resid / (100 - 3)
        cov = s2 * np.linalg.inv(x.T @ x)
        np.testing.assert_allclose(res.tstat.ravel(),
                                   res.beta.ravel() / np.sqrt(np.diag(cov)), rtol=1e-8)
        np.testing.assert_allclose(res.bint[:, 0], res.beta.ravel() - 1.96 * np.sqrt(np.diag(cov)),
                                   rtol=1e-2)

    def test_mismatched_lengths_raise(self):
        with self.assertRaises(ValueError):
            ols(np.zeros(3), np.zeros((4, 1)))


class RztcritTest(unittest.TestCase):
    def test_book_values_for_gld_gdx(self):
        # The book's example7_2 prints -3.819 / -3.343 / -3.042.
        crit = rztcrit(450, 1, 0).ravel()
        np.testing.assert_allclose(crit[:3], [-3.81898, -3.34274, -3.04197])

    def test_small_sample_bracket(self):
        np.testing.assert_allclose(rztcrit(100, 1, 0).ravel()[:3],
                                   [-4.02456, -3.40397, -3.08903])

    def test_unknown_combination_raises(self):
        with self.assertRaises(ValueError):
            rztcrit(450, 9, 0)


class CadfTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        self.assertAlmostEqual(self.res.adf, -2.14258438, places=7)
        self.assertAlmostEqual(self.res.alpha, -0.001167, places=5)
        self.assertEqual(self.res.nlag, 1)
        self.assertEqual(self.res.nvar, 1)
        self.assertEqual(self.res.meth, "cadf")

    def test_critical_values(self):
        np.testing.assert_allclose(self.res.crit.ravel()[:3],
                                   [-3.880, -3.359, -3.038], atol=1e-3)


class PrintingTest(unittest.TestCase):
    def test_mprint_formats_numbers(self):
        out = io.StringIO()
        mprint(np.array([[1.5, 2.0]]), {"fmt": "%8.2f", "fid": out})
        self.assertIn("1.50", out.getvalue())
        self.assertIn("2.00", out.getvalue())

    def test_mprint_accepts_missing_percent(self):
        out = io.StringIO()
        mprint(np.array([[1.23456789]]), {"fmt": "16.6f", "fid": out})
        self.assertIn("1.234568", out.getvalue())

    def test_mprint_writes_column_names(self):
        out = io.StringIO()
        mprint(np.array([[1.0, 2.0]]), {"cnames": ["a", "b"], "fid": out})
        self.assertIn("a", out.getvalue())
        self.assertIn("b", out.getvalue())

    def test_prt_prints_cointegration_results(self):
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
        x = np.column_stack([np.ones(10), np.arange(10.0)])
        out = io.StringIO()
        prt(ols(np.arange(10.0), x), ["const", "x1"], out)
        self.assertIn("Coefficient", out.getvalue())
        self.assertIn("R-squared", out.getvalue())

    def test_mprint_reproduces_the_book_layout(self):
        # This is the CADF table printed by the book for KO/PEP (example7_3).
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
        with self.assertRaises(ValueError):
            mprint(np.zeros((2, 3)), {"fmt": ["%5.1f", "%5.1f"],
                                      "fid": io.StringIO()})

    def test_prt_johansen(self):
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
        class Dummy:
            meth = "nope"

        with self.assertRaises(ValueError):
            prt(Dummy(), fid=io.StringIO())


if __name__ == "__main__":
    unittest.main()
