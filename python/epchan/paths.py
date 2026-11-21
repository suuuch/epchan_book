"""Locations of the code and data files that ship with the book."""

from pathlib import Path

#: Root of the git repository (the parent of the ``matlab``/``python`` folders).
REPO_ROOT = Path(__file__).resolve().parents[2]

#: Folder that holds every spreadsheet, ``.mat`` file and text export.
DATA_DIR = REPO_ROOT / "data"


def data_path(name):
    """Return the path of a data file that lives in the ``data`` folder."""
    return DATA_DIR / name


def example_path(*parts):
    """Return a path inside the ``python/examples`` directory."""
    return Path(__file__).resolve().parents[1] / "examples" / Path(*parts)
