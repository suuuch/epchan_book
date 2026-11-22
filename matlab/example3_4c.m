clear; % make sure previously defined variables are erased.
% 清空之前已定义的变量。

% Add this folder and the data folder to the MATLAB path.
% 将此文件夹和数据文件夹添加到 MATLAB 路径。
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);

cls=getCls('IGE');

dailyret=(cls(2:end)-cls(1:end-1))./cls(1:end-1); % daily returns
% 日收益率

excessRet=dailyret - 0.04/252; % excess daily returns = strategy returns - financing cost, assuming risk-free rate of 4% per annum and 252 trading days in a year
% 超额日收益率 = 策略收益率 - 融资成本，假设年无风险利率为 4%，且每年有 252 个交易日

sharpeRatio=sqrt(252)*mean(excessRet)/std(excessRet) % the output should be 0.7893
% 输出应为 0.7893

cls=getCls('SPY'); % sort cls into ascending order of dates.
% 将 cls 按日期升序排序。

dailyretSPY=(cls(2:end)-cls(1:end-1))./cls(1:end-1); % daily returns
% 日收益率

netRet=(dailyret - dailyretSPY)/2; % net daily returns (divide by 2 because we now have twice as much capital.)
% 净日收益率 (除以 2 是因为我们现在有双倍的资本)

sharpeRatio=sqrt(252)*mean(netRet)/std(netRet) % the output should be 0.7837
% 输出应为 0.7837

cumret=cumprod(1+netRet)-1; % cumulative compounded returns
% 累计复合收益率

plot(cumret);

[maxDrawdown, maxDrawdownDuration]=calculateMaxDD(cumret);

maxDrawdown % maximum drawdown. Output should be 0.1053 
% 最大回撤。输出应为 0.1053

maxDrawdownDuration % maximum drawdown duration. Output should be 497.
% 最大回撤持续时间。输出应为 497。