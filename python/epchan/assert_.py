"""Port of the MATLAB ``assert.m`` written by Ernest Chan.

ASSERT: raise an error if the predicate is not true.
        assert(pred, string)
用途: 若断言条件不成立，则抛出错误。
用法: assert(pred, string)

written by:
Ernest Chan

Author of "Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"

ernest@epchan.com
www.epchan.com
编写者：
作者：Ernest Chan
著有"Quantitative Trading:
How to Start Your Own Algorithmic Trading Business"一书

MATLAB ships its own ``assert`` but the book overrides it with a version that
accepts a message.  Python's ``assert`` is a statement, so the port lives in
``assert_``.
MATLAB 自带 ``assert`` 函数，但书中用一个可接受消息的版本覆盖了它。
Python 的 ``assert`` 是语句，因此移植版本取名 ``assert_``。
"""


def assert_(pred, msg=""):
    """Raise an ``AssertionError`` when ``pred`` is false.

    Mirrors the MATLAB ``assert(pred, str)`` helper: the error message is
    ``'assertion violated: <str>'``.
    对应 MATLAB 的 ``assert(pred, str)`` 辅助函数：错误消息为
    ``'assertion violated: <str>'``。
    """
    if not pred:
        raise AssertionError("assertion violated: %s" % msg)
