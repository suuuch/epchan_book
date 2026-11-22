clear; % make sure previously defined variables are erased.
% 清空之前已定义的变量。

% Add this folder and the data folder to the MATLAB path.
% 将本文件夹和数据文件夹添加到 MATLAB 路径中。
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);

cls=getCls('IGE');

dailyret=(cls(2:end)-cls(1:end-1))./cls(1:end-1); % daily returns
% 每日收益率

excessRet=dailyret - 0.04/252; % excess daily returns = strategy returns - financing cost, assuming risk-free rate of 4% per annum and 252 trading days in a year
% 超额每日收益率 = 策略收益率 - 融资成本，假设年化无风险利率为 4%，一年有 252 个交易日

sharpeRatio=sqrt(252)*mean(excessRet)/std(excessRet) % the output should be 0.7893
% 输出结果应为 0.7893

cls=getCls('SPY'); % sort cls into ascending order of dates.
% 按日期升序排列 cls。

dailyretSPY=(cls(2:end)-cls(1:end-1))./cls(1:end-1); % daily returns
% 每日收益率

netRet=(dailyret - dailyretSPY)/2; % net daily returns (divide by 2 because we now have twice as much capital.)
% 净每日收益率（除以 2，因为现在我们有双倍的资本。）

sharpeRatio=sqrt(252)*mean(netRet)/std(netRet) % the output should be 0.7837
% 输出结果应为 0.7837