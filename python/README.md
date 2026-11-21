# Python port of the book's MATLAB code

This directory contains a line by line Python translation of every `.m` file
in [`../matlab`](../matlab).  The package is called `epchan`; each MATLAB file
maps to a module of the same name in snake_case.

```
epchan_book/
├── matlab/                 # the original MATLAB code
├── data/                   # every data file used by both implementations
└── python/
    ├── epchan/             # the library (one module per MATLAB function)
    ├── examples/           # one script per MATLAB example
    │   ├── r2016a/         # the R2016a variant of example 3.4
    │   └── untested/       # the scripts from the original `untested` folder
    ├── tests/              # unit + end-to-end tests
    ├── run_all_examples.py # run everything and compare with the book
    └── requirements.txt
```

## Quick start

The data files (`*.xls`, `*.mat`, `*.txt`) are read straight from
[`../data`](../data) through `epchan.paths.data_path`, so nothing has to be
copied or configured.

```bash
python3 -m venv .venv
.venv/bin/pip install -r python/requirements.txt

.venv/bin/python python/examples/example7_4.py     # one example
.venv/bin/python python/run_all_examples.py        # all of them
.venv/bin/python -m unittest discover -s python/tests -v
```

## Translation conventions

* MATLAB is 1-based, numpy 0-based.  **All indexing was translated**, so the
  numbers come out identical; the comments point at the original expression.
* MATLAB's `dim` argument becomes a **0-based numpy axis**: MATLAB `dim=1`
  (down the columns of a matrix) is Python `axis=0`.
* MATLAB structures become small dataclasses with the same field names, e.g.
  `results.beta`, `results.resid`, `results.adf` (`epchan.ols.OlsResults`,
  `epchan.cadf.CadfResults`).
* A MATLAB `fid` (an integer file handle) becomes a Python file object
  (`sys.stdout` by default), so `prt(res, ["KO", "PEP"], my_file)` works.
* `matlab_compat.py` re-implements the MATLAB builtins the book relies on:
  `xlsread`, `detrend`, `intersect`, `union`, `sort` and the `\` operator.
* `rztcrit`'s two big critical value tables are generated from the MATLAB
  source itself by `tools/generate_rztcrit.py` instead of being retyped.
* Example scripts that write a file save it into [`../data`](../data)
  (`data/example3_6_positions.npz`, `data/SPX_20071123_py.mat`), mirroring the
  MATLAB behaviour and keeping all outputs in one place.

## Mapping of the files

Paths in the first column are relative to `matlab/`, the second to `python/`.

| MATLAB | Python |
| --- | --- |
| `assert.m` | `epchan/assert_.py` (`assert_`) |
| `backshift.m` | `epchan/backshift.py` |
| `beta_inv.m`, `beta_pdf.m` | `epchan/beta_inv.py`, `epchan/beta_pdf.py` |
| `cadf.m` | `epchan/cadf.py` |
| `calculateMaxDD.m` | `epchan/calculate_maxdd.py` |
| `cols.m`, `rows.m` | `epchan/cols.py`, `epchan/rows.py` |
| `fillMissingData.m` | `epchan/fill_missing_data.py` |
| `fwdshift.m` | `epchan/fwdshift.py` |
| `getCls.m`, `getTday.m` | `epchan/get_cls.py`, `epchan/get_tday.py` |
| `isLastTradingDayOfMonth.m` | `epchan/is_last_trading_day_of_month.py` |
| `lag.m`, `lag1.m` | `epchan/lag.py`, `epchan/lag1.py` |
| `mprint.m` | `epchan/mprint.py` |
| `ols.m` | `epchan/ols.py` |
| `prt.m`, `prt_coint.m` | `epchan/prt.py`, `epchan/prt_coint.py` |
| `rztcrit.m` | `epchan/rztcrit.py` + `epchan/_rztcrit_tables.py` |
| `smartcov.m` | `epchan/smartcov.py` |
| `smartmean.m`, `smartmean1.m` | `epchan/smartmean.py`, `epchan/smartmean1.py` |
| `smartstd.m`, `smartstd1.m` | `epchan/smartstd.py`, `epchan/smartstd1.py` |
| `smartsum.m` | `epchan/smartsum.py` |
| `tdiff.m`, `tdis_inv.m`, `trimr.m` | `epchan/tdiff.py`, `epchan/tdis_inv.py`, `epchan/trimr.py` |
| `getTday2.asv` | `examples/get_tday2.py` |
| `example*.m` | `examples/example*.py` |
| `r2016a/example3_4.m` | `examples/r2016a/example3_4.py` |
| `untested/*.m` | `examples/untested/*.py` |

`prt.m` calls `prt_reg.m`, which is **not** part of this repository.  Its port
(`epchan/prt_reg.py`) prints the familiar regression table so that `prt`
works for `ols` results as well.

The two spreadsheets without a matching `.m` file (`example6_2.xls` and
`SP500_20071121.xls`) have no code to port.

## Verification against the book

All examples reproduce the numbers printed in the book, with three exceptions
that come from the **data files**, not from the code:

| Example | Book | Port | Why |
| --- | --- | --- | --- |
| `example3_4` | 0.7893 | 0.7896 | `IGE.xls` was re-adjusted after the book was printed |
| `example3_4a` (IGE alone) | 0.7618 | 0.7896 | same file (the `0.7618` matches an older slice of the data) |
| `example7_2` / `example7_5` | adf `-3.35698533`, hedge `1.6766`, half-life `10.0037` | adf `-3.51764608`, hedge `1.6395`, half-life `7.8390` | `GDX.xls` in this repository starts on 2006-05-23 and has 385 rows, while the book used a series of 400-499 rows (its critical values are the 400-499 bracket) |

`example7_3` (KO/PEP) uses the same code path as `example7_2` and matches the
book to eight decimals (`-2.14258438`, AR(1) `-0.001167`, hedge `1.0114`,
critical values `-3.880 / -3.359 / -3.038`), which confirms that the
difference above is purely a data issue.

Two scripts are historical and cannot run against today's inputs, as in the
original MATLAB:

* `examples/untested/example3_1.py` scrapes a Yahoo Finance page that no longer
  exists, and
* `examples/untested/example3_7_1.py` expects a *long* format export while the
  `data/Export.txt` shipped here is the *wide* format (identical to
  `data/SPX_20071123.txt`).  It detects the wide layout and fills the price
  columns it cannot recover with `NaN`; it writes `data/SPX_20071123_py.mat` so
  the book's `data/SPX_20071123.mat` is never overwritten.

## Performance notes

`smartcov` is the only place where the MATLAB loop was restructured: the
nested `for m`/`for n` loop is replaced by two matrix products that compute the
same numerator/denominator.  A test checks the two implementations against each
other.  This turns `example7_4` from minutes into seconds.
