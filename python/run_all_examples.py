"""Run every ported example and print the numbers next to the book's values.

Usage::

    .venv/bin/python python/run_all_examples.py

Examples that need input this repository does not ship (``example3_1``, which
used to scrape Yahoo Finance) or that write files are skipped by default; pass
``--all`` to run them as well.
"""

import importlib.util
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent / "examples"
sys.path.insert(0, str(EXAMPLES_DIR.parent))


def _load(relative_path):
    path = EXAMPLES_DIR / relative_path
    name = "run_" + str(path).replace(str(EXAMPLES_DIR), "").strip("/\\").replace("/", "_")
    name = name.replace(".py", "").replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXAMPLES = [
    ("example3_4.py", "Sharpe ratio of IGE (book: 0.7893)"),
    ("example3_4a.py", "IGE vs SPY (book: 0.7618 / 0.7837)"),
    ("example3_4b.py", "same with getCls (book: 0.7893 / 0.7837)"),
    ("example3_4c.py", "maximum drawdown (book: 0.1053 / 497)"),
    ("example3_6.py", "pairs trading GLD/GDX (book: 2.3 / 1.5)"),
    ("example3_7.py", "market neutral SPX (book: 0.25 / -3.19)"),
    ("example6_3.py", "Kelly leverages (book: g=0.1529 S=0.4751)"),
    ("example7_2.py", "GLD/GDX cointegration"),
    ("example7_3.py", "KO/PEP cointegration (book: -2.14258438, 1.0114)"),
    ("example7_4.py", "factor model momentum (book: -1.8099)"),
    ("example7_5.py", "half life of the spread (book: 10.0037)"),
    ("example7_6.py", "January effect (book: -0.0244 / -0.0068 / 0.0881)"),
    ("example7_7.py", "monthly reversal (book: -0.9167 / -0.1055)"),
    ("r2016a/example3_4.py", "R2016a variant of example 3.4"),
    ("untested/example3_6_1.py", "look-ahead bias check"),
    ("untested/example7_5_1.py", "example 7.5 plus the cointegration test"),
    ("untested/example3_7_1.py", "rebuild the price matrix"),
    ("get_tday2.py", "the AutoSave draft helper"),
]

OPTIONAL = ["untested/example3_1.py"]  # needs a live Yahoo Finance page


def main(argv):
    run_all = "--all" in argv
    modules = EXAMPLES + ([(p, "Yahoo scrape (will fail, page no longer exists)")
                           for p in OPTIONAL] if run_all else [])
    for path, description in modules:
        print("\n" + "=" * 78)
        print("%s  --  %s" % (path, description))
        print("=" * 78)
        try:
            _load(path).main()
        except Exception as exc:  # keep going so one failure does not hide the rest
            print("ERROR: %s: %s" % (type(exc).__name__, exc))


if __name__ == "__main__":
    main(sys.argv[1:])
