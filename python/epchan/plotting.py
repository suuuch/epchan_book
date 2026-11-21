"""Optional plotting support for the ported examples.

The examples call :func:`get_pyplot` and simply skip the figure when
matplotlib is not installed, so that the numerical results can always be
reproduced.
"""


def get_pyplot():
    """Return ``matplotlib.pyplot`` when available, otherwise ``None``."""
    try:
        import matplotlib.pyplot as plt
        return plt
    except Exception:  # pragma: no cover - matplotlib is optional
        return None
