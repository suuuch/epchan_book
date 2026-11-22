clear;

% Add this folder and the data folder to the MATLAB path.
% 将本文件夹和数据文件夹添加到 MATLAB 路径中。
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);

inputFile=fullfile(dataDir, 'Export.txt');
outputFile=fullfile(dataDir, 'SPX_20071123_py');

[mysym, mytday, myop, myhi, mylo, mycl, myvol]=textread(inputFile, '%s %u %f %f %f %f %u', 'delimiter', ',');

% Since the single file consists of many symbols,
% we need to find the unique set of symbols.
% 由于单个文件包含许多符号，我们需要找出唯一的符号集合。
stocks=unique(mysym);
% Since the single file consists of many repeating set
% of dates for different symbols, we need to find the
% unique set of dates.
% 由于单个文件对不同符号包含许多重复的日期集合，我们需要找出唯一的日期集合。
tday=unique(mytday);

op=NaN(length(tday), length(stocks));
hi=NaN(length(tday), length(stocks));
lo=NaN(length(tday), length(stocks));
cl=NaN(length(tday), length(stocks));
vol=NaN(length(tday), length(stocks));

for s=1:length(stocks)
    stk=stocks{s};

    % find the locations (indices) of the data with
    % the current symbol.
    % 查找当前符号对应数据的位置（索引）。
    idxA=strmatch(stk, mysym, 'exact'); % find the locations (indices) of the data with
    % 查找当前符号对应数据的位置（索引）
    % the current set of dates.
    % 当前的日期集合。
    [foo, idxtA, idxtB]=intersect(mytday(idxA), tday);
    % Extract the set of prices for the current symbol
    % from the downloaded data.
    % 从下载的数据中提取当前符号对应的价格集合。
    op(idxtB, s)=myop(idxA(idxtA));
    hi(idxtB, s)=myhi(idxA(idxtA));
    lo(idxtB, s)=mylo(idxA(idxtA));
    cl(idxtB, s)=mycl(idxA(idxtA));
    vol(idxtB, s)=myvol(idxA(idxtA));
end

save(outputFile, 'tday', 'stocks', 'op', 'hi', 'lo', 'cl', 'vol');