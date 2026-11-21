"""Tests for the ``smart*`` statistics and the data readers."""

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
    def setUp(self):
        self.x = np.array([[1.0, np.nan], [3.0, np.inf], [5.0, 6.0]])

    def test_mean_along_columns_ignores_missing(self):
        np.testing.assert_allclose(smartmean(self.x, axis=0), [3.0, 6.0])

    def test_mean_along_rows(self):
        np.testing.assert_allclose(smartmean(self.x, axis=1), [1.0, 3.0, 5.5])

    def test_all_missing_slice_is_nan(self):
        y = smartmean(np.full((2, 2), np.nan), axis=0)
        self.assertTrue(np.isnan(y).all())

    def test_default_axis_is_first_non_singleton(self):
        self.assertAlmostEqual(smartmean(np.array([1.0, 2.0, 3.0])), 2.0)
        np.testing.assert_allclose(smartmean(self.x), [3.0, 6.0])

    def test_smartmean1_matches_smartmean(self):
        np.testing.assert_allclose(smartmean1(self.x, 0), smartmean(self.x, 0))


class SmartSumTest(unittest.TestCase):
    def test_sum_ignores_missing(self):
        x = np.array([[1.0, np.nan], [3.0, 4.0]])
        np.testing.assert_allclose(smartsum(x, axis=0), [4.0, 4.0])

    def test_all_missing_slice_is_nan(self):
        x = np.array([[np.nan], [np.nan]])
        self.assertTrue(np.isnan(smartsum(x, axis=0)).all())

    def test_sums_rows(self):
        np.testing.assert_allclose(smartsum(np.array([[1.0, 2.0], [3.0, np.nan]]), 1),
                                   [3.0, 3.0])


class SmartStdTest(unittest.TestCase):
    def test_normalised_by_n(self):
        x = np.array([[1.0], [3.0]])
        self.assertAlmostEqual(smartstd(x, 0)[0], 1.0)  # population std
        self.assertAlmostEqual(smartstd1(x, 0)[0], np.sqrt(2.0))  # sample std

    def test_ignores_missing(self):
        x = np.array([[1.0, np.nan], [3.0, np.nan], [5.0, 9.0]])
        np.testing.assert_allclose(smartstd(x, 0), [np.sqrt(8.0 / 3.0), 0.0])

    def test_all_missing_is_nan(self):
        self.assertTrue(np.isnan(smartstd(np.full((3, 1), np.nan), 0)).all())
        self.assertTrue(np.isnan(smartstd1(np.full((3, 1), np.nan), 0)).all())


class SmartCovTest(unittest.TestCase):
    def test_matches_matlab_algorithm(self):
        rng = np.random.default_rng(1)
        x = rng.normal(size=(30, 3))
        x[2, 1] = np.nan
        x[5, 2] = np.nan

        # Direct transcription of the MATLAB double loop.
        expected = np.full((3, 3), np.nan)
        xc = x - smartmean(x, axis=0)
        for m in range(3):
            for n in range(m, 3):
                expected[m, n] = smartmean(xc[:, m] * xc[:, n], axis=0)
                expected[n, m] = expected[m, n]

        np.testing.assert_allclose(smartcov(x), expected, equal_nan=True)

    def test_entirely_nan_column_stays_nan(self):
        x = np.array([[1.0, np.nan], [2.0, np.nan], [3.0, np.nan]])
        cov = smartcov(x)
        self.assertTrue(np.isnan(cov[1, :]).all())
        self.assertTrue(np.isnan(cov[:, 1]).all())
        self.assertAlmostEqual(cov[0, 0], 2.0 / 3.0)


class ReaderTest(unittest.TestCase):
    def test_get_tday_returns_dates_and_prices(self):
        tday, adjcls = get_tday(data_path("IGE.xls"))
        self.assertEqual(len(tday), 1504)
        self.assertEqual(len(adjcls), 1504)
        self.assertEqual(min(tday), 20011126)
        self.assertEqual(max(tday), 20071114)

    def test_get_cls_sorts_by_date(self):
        cls = get_cls(data_path("IGE.xls"))
        tday, raw = get_tday(data_path("IGE.xls"))
        self.assertEqual(len(cls), len(raw))
        # the prices must follow the ascending date order
        np.testing.assert_array_equal(cls, raw[np.argsort(tday, kind="stable")])


if __name__ == "__main__":
    unittest.main()
