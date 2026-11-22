"""Port of the MATLAB ``prt_coint.m`` written by James P. LeSage.

Prints the output of the cointegration tests (``adf``, ``cadf``, ``johansen``
and ``phillips``).
打印协整检验（``adf``、``cadf``、``johansen`` 和 ``phillips``）的输出结果。

PURPOSE: Prints output from co-integration tests
         adf,cadf,johansen,phillips
---------------------------------------------------
USAGE: prt_coint(results,vnames,fid,eflag)
       (the Python signature is prt_coint(result, vnames=None, fid=None))
Where: results = a structure returned by a co-integration test
       vnames  = an optional vector of variable names
       fid     = file-id for printing results to a file
                 (defaults to the MATLAB command window)
---------------------------------------------------
              e.g. vnames = ['y    ',
                             'x1   ',  NOTE: fixed width
                             'x2   ',        like all MATLAB
                             'cterm'];
              e.g. fid = fopen('coint.out','wr');
--------------------------------------------------
RETURNS:
       nothing, just prints the co-integration test results
--------------------------------------------------
NOTES: you may use prt_coint(results,[],fid) to print
       output to a file with no vnames
--------------------------------------------------
SEE ALSO: prt
---------------------------------------------------
用途：打印协整检验的输出结果
检验方法：adf,cadf,johansen,phillips
用法：prt_coint(results,vnames,fid,eflag)
      （Python 的函数签名为 prt_coint(result, vnames=None, fid=None)）
其中：results = 协整检验返回的结构体
      vnames  = 可选的变量名向量
      fid     = 将结果打印到文件所使用的文件标识
      （默认打印到 MATLAB 命令窗口）
      例如 vnames = ['y    ',
                     'x1   ',  注意：固定宽度
                     'x2   ',        与所有 MATLAB 相同
                     'cterm'];（变量名列表到此结束）
      例如 fid = fopen('coint.out','wr');
返回：
无返回值，仅打印协整检验的结果
注意：可以使用 prt_coint(results,[],fid) 把输出打印到文件中，而不使用 vnames
参见：prt

written by:
James P. LeSage, Dept of Economics
University of Toledo
2801 W. Bancroft St,
Toledo, OH 43606
jlesage@spatial-econometrics.com
编写者：
James P. LeSage（经济学系）
托莱多大学
地址：2801 W. Bancroft St,
托莱多，OH 43606

revised 10/10/2000
to fix error in mprint fid
Thanks to JChapman@bank-banque-canada.ca
for pointing out this error
修订于 10/10/2000
修正 mprint fid 中的错误
感谢 JChapman@bank-banque-canada.ca
指出该错误
"""

import sys

import numpy as np

from .mprint import mprint


def _write(fid, text):
    fid.write(text)


def prt_coint(result, vnames=None, fid=None):
    """Print the results of a cointegration test.

    ``result`` is the structure returned by :func:`epchan.cadf` (or by the
    ``adf``/``phillips``/``johansen`` tests), ``vnames`` an optional list with
    the names of the variables and ``fid`` the file object to write to.

    ``result`` 是 :func:`epchan.cadf`（或 ``adf``/``phillips``/``johansen``
    检验）返回的结构体，``vnames`` 是可选的变量名列表，``fid`` 是写入的
    文件对象。
    """
    # if nargin < 1; error('wrong # of arguments to prt_coint'); end;
    # 检查参数个数：if nargin < 1; error('wrong # of arguments to prt_coint'); end;
    if fid is None:
        fid = sys.stdout

    # user may supply a blank argument
    # 用户可以传入一个空参数
    nflag = 1 if (vnames is not None and len(vnames) > 0) else 0

    meth = getattr(result, "meth", None)
    if meth == "johansen":
        return _prt_johansen(result, vnames, fid, nflag)
    if meth == "adf":
        return _prt_adf(result, vnames, fid, nflag)
    if meth == "cadf":
        return _prt_cadf(result, vnames, fid, nflag)
    if meth == "phillips":
        return _prt_phillips(result, vnames, fid, nflag)
    raise ValueError("results structure not known by prt_coint function")


def _generic_names(count):
    # make some up variable names
    # 自行构造变量名
    return ["variable   %d" % (i + 1) for i in range(count)]


def _prt_cadf(result, vnames, fid, nflag):
    if nflag == 0:
        # no variable names supplied, make some up
        # 未提供变量名，自行构造
        vname = _generic_names(2)
    else:
        # the user supplied variable names
        # 用户提供了变量名
        if len(vnames) != 2:
            raise ValueError(
                "Wrong # of variable names in prt_coint -- check vnames argument")
        # truncate vnames to 16-characters
        # 将 vnames 截断为 16 个字符
        vname = [str(v)[:16] for v in vnames]
    # end of nflag issue
    # nflag 处理结束

    _write(fid, "\n Augmented DF test for co-integration")
    _write(fid, " variables: %30s  \n" % ("%s,%s" % (vname[0], vname[1])))

    mprint(np.array([[result.adf, result.nlag, result.alpha]]),
           {"cnames": ["CADF t-statistic", "# of lags", "AR(1) estimate"],
            "fmt": ["%16.8f", "%10d", "%16.6f"],
            "fid": fid})

    mprint(np.asarray(result.crit).ravel()[0:3].reshape(1, 3),
           {"cnames": ["1% Crit Value", "5% Crit Value", "10% Crit Value"],
            "fmt": "%16.3f",
            "fid": fid})


def _prt_adf(result, vnames, fid, nflag):
    if nflag == 0:
        # no variable names supplied, make some up
        # 未提供变量名，自行构造
        vname = _generic_names(1)
    else:
        # the user supplied variable names
        # 用户提供了变量名
        # truncate vnames to 16-characters
        # 将 vnames 截断为 16 个字符
        vname = [str(vnames[0])[:16]]
    # end of nflag issue
    # nflag 处理结束

    _write(fid, "\nAugmented DF test for unit root variable: %30s \n" % vname[0])

    mprint(np.array([[result.adf, result.nlag, result.alpha]]),
           {"cnames": ["ADF t-statistic", "# of lags", "AR(1) estimate"],
            "fmt": ["%16.6f", "%10d", "%16.6f"],
            "fid": fid})

    mprint(np.asarray(result.crit).ravel()[0:3].reshape(1, 3),
           {"cnames": ["1% Crit Value", "5% Crit Value", "10% Crit Value"],
            "fmt": "%16.3f",
            "fid": fid})


def _prt_phillips(result, vnames, fid, nflag):
    if nflag == 0:
        # no variable names supplied, make some up
        # 未提供变量名，自行构造
        vname = _generic_names(2)
    else:
        # the user supplied variable names
        # 用户提供了变量名
        if len(vnames) != 2:
            raise ValueError(
                "Wrong # of variable names in prt_coint -- check vnames argument")
        # truncate vnames to 16-characters
        # 将 vnames 截断为 16 个字符
        vname = [str(v)[:16] for v in vnames]
    # end of nflag issue
    # nflag 处理结束

    _write(fid, "\n Phillips-Peron test for co-integration")
    _write(fid, " variables: %30s  \n" % ("%s,%s" % (vname[0], vname[1])))

    mprint(np.array([[result.pstat, result.nlag, result.alpha]]),
           {"cnames": ["Phillips-Peron statistic", "# of lags", "AR(1) estimate"],
            "fmt": ["%16.8f", "%10d", "%16.6f"],
            "fid": fid})

    mprint(np.asarray(result.crit).ravel()[0:3].reshape(1, 3),
           {"cnames": ["1% Crit Value", "5% Crit Value", "10% Crit Value"],
            "fmt": "%16.3f",
            "fid": fid})


def _as_column(values):
    """Return ``values`` as an ``(n, 1)`` matrix (no-op for a 2-D input).

    将 ``values`` 转换为 ``(n, 1)`` 矩阵（对二维输入为空操作）。
    """
    values = np.asarray(values, dtype=float)
    if values.ndim == 1:
        values = values.reshape(-1, 1)
    return values


def _prt_johansen(result, vnames, fid, nflag):
    eig = np.asarray(result.eig)
    # MATLAB's ``[nvar junk] = size(result.eig)``
    # MATLAB 中的 ``[nvar junk] = size(result.eig)``
    nvar = eig.shape[0]
    # recover variable order index
    # 恢复变量顺序索引
    index = np.asarray(result.ind).ravel()

    if nflag == 1:
        # the user supplied variable names
        # 用户提供了变量名
        vnames = np.asarray(vnames)
        if vnames.shape[0] != nvar:
            _write(
                fid,
                "Wrong # of variable names in prt_coint -- check vnames argument \n")
            _write(fid, "will use generic variable names \n")
            nflag = 0
        else:
            # recover variable order index
            # 恢复变量顺序索引
            vname = [str(vnames[i - 1]) for i in index]
    if nflag == 0:
        # make some up variable names
        # 自行构造变量名
        vname = ["variable   %d" % i for i in index]
    # end of nflag issue
    # nflag 处理结束

    rname = ["NULL:"]
    for i in range(nvar):
        rname.append("r <= %d   %s" % (i, vname[i]))

    _write(fid, "\n Johansen MLE estimates \n")
    # MATLAB: prtmat = [result.lr1 result.cvt]
    # MATLAB 中: prtmat = [result.lr1 result.cvt]
    mprint(np.hstack([_as_column(result.lr1), _as_column(result.cvt)]),
           {"cnames": ["Trace Statistic", "Crit 90%", "Crit 95%", "Crit 99%"],
            "rnames": rname,
            "fmt": "%16.3f",
            "fid": fid})
    mprint(np.hstack([_as_column(result.lr2), _as_column(result.cvm)]),
           {"cnames": ["Eigen Statistic", "Crit 90%", "Crit 95%", "Crit 99%"],
            "rnames": rname,
            "fmt": "%16.3f",
            "fid": fid})
    # end of Johansen
    # Johansen 部分结束
