"""Port of the MATLAB ``prt.m`` written by James P. LeSage.

``prt`` is a thin wrapper that looks at the ``meth`` field of a results
structure and calls the matching printing routine.
``prt`` 是一个简单的包装函数，它查看结果结构体的 ``meth`` 字段，
并调用与之匹配的打印例程。

PURPOSE: Prints results structures returned by most functions
         by calling the appropriate printing function
---------------------------------------------------
USAGE: prt(results,vnames,fid)
Where: results = a results structure returned an econometric function
       vnames  = an optional vector of variable names
       fid     = file-id for printing results to a file
                 (defaults to the MATLAB command window)
---------------------------------------------------
              e.g. vnames = ['y    ',
                             'x1   ',  NOTE: fixed width
                             'x2   ',        like all MATLAB
                             'cterm'];       strings
              e.g. fid = fopen('ols.out','wr');
--------------------------------------------------
NOTES: you may use prt(results,[],fid) to print
       output to a file with no vnames
       this is simply a wrapper function that calls another function
--------------------------------------------------
RETURNS:
       nothing, just prints the regression results
--------------------------------------------------
SEE ALSO: plt()
---------------------------------------------------
用途: 打印大多数函数返回的结果结构
通过调用相应的打印函数实现
用法: prt(results,vnames,fid)
其中: results = 计量经济学函数返回的结果结构
      vnames = 可选的变量名向量
      fid = 用于将结果打印到文件的文件标识符
      (默认为 MATLAB 命令窗口)
      例如 vnames = ['y    ',
                     'x1   ',  注意: 固定宽度
                     'x2   ',        与所有 MATLAB
                     'cterm'];       字符串相同
      例如 fid = fopen('ols.out','wr');
注意: 可以使用 prt(results,[],fid) 将输出打印到文件, 不带 vnames
      本函数只是一个调用其他函数的包装函数
返回:
无返回值, 仅打印回归结果
参见: plt()

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jlesage@spatial-econometrics.com
编写者:
"""

import sys

from .prt_coint import prt_coint
from .prt_reg import prt_reg

#: The methods understood by ``prt``.
#: ``prt`` 能够识别的估计方法。
_COINT_METHODS = ("johansen", "adf", "cadf", "phillips")
_REG_METHODS = ("arma", "boxcox", "boxcox2", "hwhite", "lad", "logit", "mlogit",
                "nwest", "ols", "olsc", "olsar1", "olst", "probit", "ridge",
                "robust", "theil", "tobit", "tsls")


def prt(results, vnames=None, fid=None):
    """Print a results structure.

    ``results`` is the structure returned by one of the econometric helpers
    (``ols``, ``cadf``, ...), ``vnames`` an optional list of variable names
    and ``fid`` the file object the output is written to.

    ``results`` 是某个计量经济学辅助函数（``ols``、``cadf`` 等）返回的
    结构体，``vnames`` 是可选的变量名列表，``fid`` 是写入输出的文件对象。
    """
    if fid is None:
        fid = sys.stdout

    meth = getattr(results, "meth", None)
    if meth is None:
        raise ValueError("prt: requires a structure input")

    # call prt_coint
    # 调用 prt_coint
    if meth in _COINT_METHODS:
        prt_coint(results, vnames, fid)
    # call prt_reg
    # 调用 prt_reg
    elif meth in _REG_METHODS:
        prt_reg(results, vnames, fid)
    else:
        raise ValueError("results structure not known by prt function")
