"""Tests for the beta and Student t quantile helpers."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from scipy import stats

from epchan.beta_inv import beta_inv
from epchan.beta_pdf import beta_pdf
from epchan.tdis_inv import tdis_inv


class BetaPdfTest(unittest.TestCase):
    def test_matches_scipy(self):
        x = np.array([0.1, 0.3, 0.5, 0.9])
        np.testing.assert_allclose(beta_pdf(x, 2.0, 3.0), stats.beta.pdf(x, 2.0, 3.0))

    def test_outside_support_is_zero(self):
        np.testing.assert_array_equal(beta_pdf(np.array([-0.1, 1.1]), 2.0, 3.0), [0.0, 0.0])

    def test_nonpositive_parameter_raises(self):
        with self.assertRaises(ValueError):
            beta_pdf(np.array([0.5]), 0.0, 1.0)


class BetaInvTest(unittest.TestCase):
    def test_matches_scipy(self):
        p = np.array([0.01, 0.25, 0.5, 0.75, 0.99])
        np.testing.assert_allclose(beta_inv(p, 2.0, 5.0), stats.beta.ppf(p, 2.0, 5.0),
                                   rtol=1e-8)

    def test_probability_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            beta_inv(np.array([1.5]), 2.0, 3.0)


class TdisInvTest(unittest.TestCase):
    def test_matches_scipy(self):
        for p in (0.001, 0.025, 0.05, 0.95, 0.975, 0.999):
            for dof in (5, 30, 500):
                self.assertAlmostEqual(float(tdis_inv(p, dof)), float(stats.t.ppf(p, dof)),
                                       places=9)

    def test_symmetry(self):
        self.assertAlmostEqual(float(tdis_inv(0.025, 100)), -float(tdis_inv(0.975, 100)),
                               places=12)


if __name__ == "__main__":
    unittest.main()
