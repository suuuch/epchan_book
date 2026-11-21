# epchan_book

Source code and data for Ernest P. Chan's book
*Quantitative Trading: How to Build Your Own Algorithmic Trading Business*.

The repository contains the original **MATLAB** code, a **Python port** of the
same code, and all the **data** files, in three separate top-level folders.
Both implementations read the data from `data/` and reproduce the numbers
printed in the book (see [Verification](#verification)).

## Layout

```
epchan_book/
├── matlab/                 # 48 MATLAB files: 29 helper functions, 18 examples,
│   │                       #   plus getTday2.asv
│   ├── r2016a/
│   │   └── example3_4.m    # the R2016a variant of example 3.4
│   └── untested/           # example3_1, example3_6_1, example3_7_1, example7_5_1
├── python/                 # the Python port (see python/README.md)
│   ├── epchan/             # library: one module per MATLAB function
│   ├── examples/           # one script per MATLAB example
│   ├── tests/              # 101 unit and end-to-end tests
│   ├── tools/              # generate_rztcrit.py
│   └── run_all_examples.py # run the examples next to the book's numbers
└── data/                   # 27 spreadsheets, .mat files and text exports
```

## Python

Requirements: Python 3.9+ with `numpy`, `scipy` and `xlrd`; `matplotlib` is
optional and only used to draw the figures.

```bash
python3 -m venv .venv
.venv/bin/pip install -r python/requirements.txt

.venv/bin/python python/examples/example7_4.py      # one example
.venv/bin/python python/run_all_examples.py         # all of them
.venv/bin/python -m unittest discover -s python/tests -v
```

The package mirrors the MATLAB file names (`calculateMaxDD.m` →
`epchan.calculate_maxdd`), keeps MATLAB's `results.beta` / `results.adf`
field names in small dataclasses, and translates all indexing (MATLAB is
1-based, numpy 0-based), so the results are identical. MATLAB's `dim` argument
becomes a 0-based numpy `axis`. See
[`python/README.md`](python/README.md) for the full file-by-file mapping.

## MATLAB

All `.m` files live in `matlab/`.  Each example script adds its own folder and
`../data` to the MATLAB path at the top, so it can be run from anywhere:

```matlab
cd matlab
example3_4
```

The path setup is

```matlab
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);
```

It only uses functions that exist in MATLAB R13, which this code still
supports, so the original `xlsread('IGE')`, `load('SPX_20071123')` and
`getTday('GLD')` calls keep working unchanged.  Note that

* `example3_6.m` writes `data/example3_6_positions.mat`, which
  `untested/example3_6_1.m` reads for the look-ahead bias check;
* `untested/example3_7_1.m` reads `data/Export.txt` and writes
  `data/SPX_20071123_py.mat` (so the book's `SPX_20071123.mat` is never
  overwritten).

## Data

Both implementations read the files in `data/` directly; nothing has to be
copied.  The folder holds:

* Yahoo Finance exports, one per symbol: `IGE.xls`, `SPY.xls`, `GLD.xls`,
  `GDX.xls`, `KO.xls`, `PEP.xls`, `OIH.xls`, `RKH.xls`, `RTH.xls`, plus the
  tab-separated `.txt` copies and the wide matrices `IJR_20080114.txt`,
  `IJR_20080131.txt`, `SPX_20071123.txt`, `SPX_op_20071123.txt`,
  `Export.txt`;
* MATLAB matrices: `SPX_20071123.mat`, `IJR_20080114.mat`,
  `IJR_20080131.mat`;
* a few extra spreadsheets that come with the book (`example3_4.xls`,
  `example6_2.xls`, `SP500_20071121.xls`) and the saved
  `example3_6_positions.mat`.

`data/Export.txt` and `data/example3_6_positions.mat` originally lived in the
`untested/` folder; they were moved here so that all input and output data
sits in one place.

## Verification

`example7_3` matches the book to eight decimals, and the following examples
reproduce the printed output exactly:

| Example | Quantity | Book | This repo |
| --- | --- | --- | --- |
| 3.4c | maximum drawdown / duration | `0.1053` / `497` | `0.1053` / `497` |
| 3.6 | Sharpe ratio, train / test | ≈ `2.3` / ≈ `1.5` | `2.3325` / `1.5139` |
| 3.7 | Sharpe ratio, with / without costs | ≈ `0.25` / ≈ `-3.19` | `0.2515` / `-3.1886` |
| 6.3 | growth rate / portfolio Sharpe | `0.1529` / `0.4751` | `0.1529` / `0.4751` |
| 7.3 | CADF t-stat, hedge ratio | `-2.14258438`, `1.0114` | identical |
| 7.4 | annualised return | `-1.8099` | `-1.8099` |
| 7.6 | 2005 / 2006 / 2007 portfolio return | `-0.0244`, `-0.0068`, `0.0881` | identical |
| 7.7 | average annual return / Sharpe | `-0.9167`, `-0.1055` | identical |

Three results differ from the book because the **data files** were refreshed
after it was printed, not because of the code:

| Example | Book | This repo | Why |
| --- | --- | --- | --- |
| 3.4, 3.4a, 3.4b, r2016a | `0.7893` (`0.7618` in 3.4a / r2016a) | `0.7896` | `IGE.xls` was re-adjusted in 2019 |
| 7.2, 7.5, untested/7_5_1 | CADF `-3.35698533`, hedge `1.6766`, half-life `10.0037` | CADF `-3.51764608`, hedge `1.6395`, half-life `7.8390` | `GDX.xls` starts on 2006-05-23 and has 385 rows; the book used a 400–499 row series (its critical values are the 400–499 bracket) |
| untested/3_6_1 | ≈ `2.9` / ≈ `1.0` | `2.3325` / `0.8774` | same GLD/GDX data difference |

`example7_3` uses the same `cadf`/`ols` code path as `example7_2` and matches
the book exactly, which confirms that the differences above are data issues.

## Notes

* The original repository does not ship `prt_reg.m`, although `prt.m` calls it
  for every regression result.  The Python port provides
  `epchan/prt_reg.py` so that `prt` works for `ols` results too.
* `untested/example3_1` scrapes a Yahoo Finance page that no longer exists;
  it is kept as a faithful historical script in both languages.
* `untested/example3_7_1` expects a *long* format export, while the shipped
  `data/Export.txt` is the *wide* format (identical to
  `data/SPX_20071123.txt`).  The Python port detects the wide layout, fills
  the price columns it cannot recover with `NaN`, and writes
  `data/SPX_20071123_py.mat`.
* The Python port regenerates `epchan/_rztcrit_tables.py` (the two large
  critical-value tables) straight from `matlab/rztcrit.m` with
  `python/tools/generate_rztcrit.py`.

## License

See [`LICENSE`](LICENSE).
