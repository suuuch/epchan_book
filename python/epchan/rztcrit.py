"""Port of the MATLAB ``rztcrit.m`` written by James P. LeSage.

Critical values for the ``Zt`` statistic used by :func:`epchan.cadf`.
"""

from ._rztcrit_tables import TABLES


def rztcrit(nobs, k, p):
    """Return the 6 critical values used by the augmented Dickey-Fuller test.

    ``nobs`` is the number of observations, ``k`` the number of variables of
    the ``x`` matrix and ``p`` the order of the time polynomial of the null
    hypothesis (``-1`` none, ``0`` constant, ``1`` constant plus trend).

    The returned vector holds the ``[1% 5% 10% 90% 95% 99%]`` quintiles.

    Unlike the MATLAB original, which silently indexes past the end of the
    table when ``k`` or ``p`` is out of range, a ``ValueError`` is raised for
    combinations that are not tabulated.
    """
    nobs = int(nobs)
    k = int(k)
    p = int(p)

    table = None
    for _name, (low, high), values in TABLES:
        if nobs >= low and (high is None or nobs <= high):
            table = values
            break
    if table is None:
        raise ValueError("no critical values available for nobs=%d" % nobs)

    # The MATLAB code computes the row index as n = (k-1)*7 + p + 2.
    n = (k - 1) * 7 + p + 2
    if n < 1 or n > table.shape[0]:
        raise ValueError(
            "critical values are not tabulated for k=%d and p=%d" % (k, p))
    return table[n - 1, :].reshape(6, 1)
