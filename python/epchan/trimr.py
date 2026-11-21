"""Port of the MATLAB ``trimr.m`` (Gauss' ``trimr``)."""

import numpy as np


def trimr(x, n1, n2):
    """Strip the first ``n1`` and the last ``n2`` rows of ``x``.

    MATLAB's ``z = x(n1+1:n-n2,:)`` translates to ``x[n1:len(x)-n2]`` in
    Python because both bounds are exclusive.
    """
    x = np.asarray(x)
    n = x.shape[0]
    if n1 + n2 >= n:
        raise ValueError("Attempting to trim too much in trimr")
    return x[n1:n - n2]
