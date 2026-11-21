# epchan_book

Source code and data of Ernest P. Chan's book
*Quantitative Trading: How to Build Your Own Algorithmic Trading Business*.

The repository is split into three top level folders:

```
epchan_book/
├── matlab/     # the original MATLAB code (one .m file per function / example)
│   ├── r2016a/ # the R2016a variant of example 3.4
│   └── untested/
├── python/     # the Python port of the same code (see python/README.md)
└── data/       # every spreadsheet, .mat file and text export used by both
```

## MATLAB

All `.m` files live in `matlab/`.  Every example script adds its own folder and
`../data` to the MATLAB path, so it can be run from anywhere:

```matlab
cd matlab
example3_4          % or: run('matlab/example3_4.m') from the repository root
```

The path setup at the top of each script is

```matlab
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);
```

It relies only on functions that exist in MATLAB R13, which this code still
supports.  Note that `example3_6.m` writes `data/example3_6_positions.mat`
(used by `untested/example3_6_1.m` for the look-ahead bias check).

## Python

See [`python/README.md`](python/README.md).  Quick start:

```bash
python3 -m venv .venv
.venv/bin/pip install -r python/requirements.txt
.venv/bin/python python/run_all_examples.py
```

## Data

Both implementations read the files in `data/` directly; nothing has to be
copied.  `data/Export.txt` (the wide export of SP500 prices) and
`data/example3_6_positions.mat` originally lived in the `untested/` folder and
were moved here so that all input/output data sits in one place.
