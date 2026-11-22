% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% 编写者: Ernest Chan
% “Quantitative Trading: How to Start Your Own Algorithmic Trading Business”的作者

clear;

% Add this folder and the data folder to the MATLAB path.
% 将此文件夹和数据文件夹添加到 MATLAB 路径。
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);

load('SPX_20071123', 'tday', 'stocks', 'cl');

monthEnds=find(isLastTradingDayOfMonth(tday)); % find the indices of the days that are at month ends.
% 查找处于月末的交易日索引。

monthlyRet=(cl(monthEnds, :)-lag1(cl(monthEnds, :)))./lag1(cl(monthEnds, :));

mycl=fillMissingData(cl);

% myMonthlyRet=(mycl(monthEnds, :)-lag1(mycl(monthEnds, :)))./lag1(mycl(monthEnds, :));
% 用 mycl 计算月度收益率: myMonthlyRet=(mycl(monthEnds, :)-lag1(mycl(monthEnds, :)))./lag1(mycl(monthEnds, :));

[monthlyRetSorted sortIndex]=sort(monthlyRet, 2); % sort stocks by monthly returns in ascending order
% 按月度收益率升序对股票排序

prevYearMonthlyRetSorted=backshift(12, monthlyRetSorted); % these are the sorted monthly returns of the previous year
% 上一年度排序后的月度收益率
prevYearSortIndex=backshift(12, sortIndex); % the sort index of the previous year
% 上一年度的排序索引

positions=zeros(size(monthlyRet));

for m=13:size(monthlyRet, 1)
    hasReturns=isfinite(prevYearMonthlyRetSorted(m, :)) & isfinite(cl(monthEnds(m-1), :));
    mySortIndex=prevYearSortIndex(m, hasReturns);
    
    topN=floor(length(mySortIndex)/10); % take top decile of stocks as longs, bottom decile as shorts 
    % 取最高的十分之一股票做多，最低的十分之一股票做空
    
    positions(m-1, mySortIndex(1:topN))=-1;
    positions(m-1, mySortIndex(end-topN+1:end))=1;       
end

ret=smartsum(lag1(positions).*monthlyRet, 2);

avgannret=12*smartmean(ret);
sharpe=sqrt(12)*smartmean(ret)/smartstd(ret);

fprintf(1, 'Avg ann return=%7.4f Sharpe ratio=%7.4f\n', avgannret, sharpe);
% Output should be
% Avg ann return=-0.9167 Sharpe ratio=-0.1055
% 输出应为年化平均收益率=-0.9167 夏普比率=-0.1055
