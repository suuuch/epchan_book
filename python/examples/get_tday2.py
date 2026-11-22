"""Port of ``getTday2.asv``.

``.asv`` is MATLAB's AutoSave extension, and the saved draft contains a syntax
error (``tmp1(k) = mod(tday(k),1000;`` has a missing closing parenthesis), so
the original function never ran.  The evident intent was to turn ``yyyymmdd``
day numbers into MATLAB date strings; this port does exactly that and returns
the dates formatted the way ``datestr`` formats them by default
(``dd-mmm-yyyy``).

``.asv`` 是 MATLAB 的自动保存扩展名，这个保存的草稿里有一个语法错误
（``tmp1(k) = mod(tday(k),1000;`` 缺少右括号），所以原函数从未运行过。
它显然是想把 ``yyyymmdd`` 格式的日期数字转换成 MATLAB 日期字符串；
本移植正是这样做的，返回的日期按 ``datestr`` 的默认格式
（``dd-mmm-yyyy``）排列。
"""

import datetime as _dt

import numpy as np


def get_tday2(tday):
    """Convert ``yyyymmdd`` day numbers into ``dd-mmm-yyyy`` strings.

    ``tday`` may be a scalar, a list or an array; a list of strings is always
    returned, mirroring ``cellstr(datestr(...))``.

    将 ``yyyymmdd`` 格式的日期数字转换成 ``dd-mmm-yyyy`` 格式的字符串。

    ``tday`` 可以是标量、列表或数组；始终返回字符串列表，
    与 ``cellstr(datestr(...))`` 一致。
    """
    # tday=datestr(tday, 'yyyymmdd');
    # 把日期格式化为 yyyymmdd。
    # tday=datestr(tday, 'yyyymmddTHHMMSS');
    # 把日期格式化为 yyyymmddTHHMMSS。

    # len=length(tday);
    # 取日期序列的长度。
    # tdaycell = cell(len, 1);
    # 建立长度为 len 的单元格数组。
    # for k=1:1:len
    # 逐个遍历每一个日期。
    #     tdaycell{k,1} = tday(k, 1:8);
    # 取每个日期的前 8 个字符，即 yyyymmdd。
    # end

    # tmp1=cellstr(num2str(tday));
    # 把日期数字先转成字符串数组。
    # tmp1=num2str(tday);
    # 或者直接用 num2str 转成字符矩阵。

    values = np.atleast_1d(np.asarray(tday)).ravel()
    out = []
    for value in values:
        # tmp1(k) = strcat(tmp1(k),'T000000');
        # 给日期字符串补上时间部分 T000000。
        value = int(value)
        try:
            day = _dt.date(value // 10000, (value // 100) % 100, value % 100)
        except ValueError:
            out.append("")
            continue
        out.append(day.strftime("%d-%b-%Y"))
    return out


def main():
    """Print a small demonstration, mirroring the script-like ``.asv`` file.

    打印一个小的演示，模仿那个类似脚本的 ``.asv`` 文件。
    """
    values = [20071123, 20051130]
    print(get_tday2(values))
    return get_tday2(values)


if __name__ == "__main__":
    main()
