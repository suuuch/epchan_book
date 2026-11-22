"""Locations of the code and data files that ship with the book.

随书附带的代码文件与数据文件所在的位置。
"""

from pathlib import Path

#: Root of the git repository (the parent of the ``matlab``/``python`` folders).
#: git 仓库的根目录（``matlab``/``python`` 两个文件夹的父目录）。
REPO_ROOT = Path(__file__).resolve().parents[2]

#: Folder that holds every spreadsheet, ``.mat`` file and text export.
#: 保存全部电子表格、``.mat`` 文件和文本导出文件的文件夹。
DATA_DIR = REPO_ROOT / "data"


def data_path(name):
    """Return the path of a data file that lives in the ``data`` folder.

    返回位于 ``data`` 文件夹中的数据文件的路径。
    """
    return DATA_DIR / name


def example_path(*parts):
    """Return a path inside the ``python/examples`` directory.

    返回 ``python/examples`` 目录内部的路径。
    """
    return Path(__file__).resolve().parents[1] / "examples" / Path(*parts)
