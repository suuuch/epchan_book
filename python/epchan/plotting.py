"""Optional plotting support for the ported examples.

The examples call :func:`get_pyplot` and simply skip the figure when
matplotlib is not installed, so that the numerical results can always be
reproduced.

移植后的示例程序所用的可选绘图支持。

示例程序调用 :func:`get_pyplot`，当没有安装 matplotlib 时就直接跳过画图，
从而保证数值结果始终可以复现。
"""


def get_pyplot():
    """Return ``matplotlib.pyplot`` when available, otherwise ``None``.

    如果 matplotlib 可用则返回 ``matplotlib.pyplot``，否则返回 ``None``。
    """
    try:
        import matplotlib.pyplot as plt
        return plt
    except Exception:  # pragma: no cover - matplotlib is optional
        return None
