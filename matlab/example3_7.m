% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% 编写者:
% 作者: 《Quantitative Trading: How to Start Your Own Algorithmic Trading Business》

clear;

% Add this folder and the data folder to the MATLAB path.
% 将本文件夹和数据文件夹添加到 MATLAB 路径中。
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);

startDate=20060101;
endDate=20061231;

load('SPX_20071123', 'tday', 'stocks', 'cl');
% save('myfile.mat','-v6');
% 保存数据: save('myfile.mat','-v6');

dailyret=(cl-lag1(cl))./lag1(cl); % daily returns
% 每日收益率

marketDailyret=smartmean(dailyret, 2); % equal weighted market index return
% 等权重市场指数收益率

weights=-(dailyret-repmat(marketDailyret, [1 size(dailyret, 2)]))./repmat(smartsum(isfinite(cl), 2), [1 size(dailyret, 2)]); % weight of a stock is proportional to the negative distance to the market index.
% 个股权重与到市场指数的负距离成正比。

weights(~isfinite(cl) | ~isfinite(lag1(cl)))=0; % those stocks that do not have valid prices or daily returns are excluded.
% 价格或每日收益率无效的股票将被剔除。

dailypnl=smartsum(lag1(weights).*dailyret, 2);

dailypnl(tday < startDate | tday > endDate) = []; % remove pnl outside of our dates of interest
% 剔除所关注日期范围之外的盈亏

sharpe=sqrt(252)*smartmean(dailypnl, 1)/smartstd(dailypnl, 1) % Sharpe ratio should be about 0.25
% 夏普比率应约为 0.25

% daily pnl with transaction costs deducted
% 扣除交易成本后的每日盈亏
onewaytcost=0.0005; % assume 5 basis points
% 假设为 5 个基点

weights(tday < startDate | tday > endDate, :) = []; % remove weights outside of our dates of interest
% 剔除所关注日期范围之外的权重

dailypnlminustcost=dailypnl - smartsum(abs(weights-lag1(weights)), 2).*onewaytcost; % transaction costs are only incurred when the weights change
% 只有在权重发生变化时才会产生交易成本

sharpeminustcost=sqrt(252)*smartmean(dailypnlminustcost, 1)/smartstd(dailypnlminustcost, 1) % Sharpe ratio should be about -3.19
% 夏普比率应约为 -3.19
