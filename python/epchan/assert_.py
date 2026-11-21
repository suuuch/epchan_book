"""Port of the MATLAB ``assert.m`` written by Ernest Chan.

MATLAB ships its own ``assert`` but the book overrides it with a version that
accepts a message.  Python's ``assert`` is a statement, so the port lives in
``assert_``.
"""


def assert_(pred, msg=""):
    """Raise an ``AssertionError`` when ``pred`` is false.

    Mirrors the MATLAB ``assert(pred, str)`` helper: the error message is
    ``'assertion violated: <str>'``.
    """
    if not pred:
        raise AssertionError("assertion violated: %s" % msg)
