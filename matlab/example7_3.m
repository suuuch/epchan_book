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
% 作者: “Quantitative Trading: How to Start Your Own Algorithmic Trading Business”

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
 
%[num, txt]=xlsread('KO'); % read a spreadsheet named "KO.xls" into MATLAB. 
% 将名为 "KO.xls" 的电子表格读入 MATLAB。
 
%tday1=txt(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。
 
%tday1=datestr(datenum(tday1, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将格式转换为 yyyymmdd。
 
%tday1=str2double(cellstr(tday1)); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，然后再转换为数值格式。
 
%adjcls1=num(:, end); % the last column contains the adjusted close prices.
% 最后一列包含复权后收盘价。

[tday1, adjcls1]=getTday('KO');

%[num2, txt2]=xlsread('PEP'); % read a spreadsheet named "PEP.xls" into MATLAB. 
% 将名为 "PEP.xls" 的电子表格读入 MATLAB。
 
%tday2=txt2(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。
 
%tday2=datestr(datenum(tday2, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将格式转换为 yyyymmdd。
 
%tday2=str2double(cellstr(tday2)); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，然后再转换为数值格式。

%adjcls2=num2(:, end);
% 复权后收盘价: adjcls2=num2(:, end);

[tday2, adjcls2]=getTday('PEP');

tday=union(tday1, tday2); % find all the days when either KO or PEP has data.
% 找出 KO 或 PEP 有数据的所有交易日。

[foo idx idx1]=intersect(tday, tday1);

%adjcls=NaN(length(tday), 2); % combining the two price series
% 合并两个价格序列
tmp=[length(tday), 2];
tmp(1:length(tday),1:2)=NaN;
adjcls=tmp;

adjcls(idx, 1)=adjcls1(idx1);

[foo idx idx2]=intersect(tday, tday2);

adjcls(idx, 2)=adjcls2(idx2);

baddata=find(any(~isfinite(adjcls), 2)); % days where any one price is missing
% 任一价格缺失的交易日

tday(baddata)=[];

adjcls(baddata, :)=[];

vnames=strvcat('KO', 'PEP');

res=cadf(adjcls(:, 1), adjcls(:, 2), 0, 1); % run cointegration check using augmented Dickey-Fuller test
% 用增广 Dickey-Fuller 检验做协整检验

prt(res, vnames); 

% Output from cadf function:
% cadf 函数的输出:

%  Augmented DF test for co-integration variables:                        KO ,PEP  
% CADF t-statistic        # of lags   AR(1) estimate 
%      -2.14258438                1        -0.001167 
% 
%    1% Crit Value    5% Crit Value   10% Crit Value 
%           -3.880           -3.359           -3.038 
% 协整变量的增广 DF 检验:              KO ,PEP
% CADF t 统计量        滞后阶数   AR(1) 估计值
% 1% 临界值    5% 临界值   10% 临界值


% The t-statistic of -2.14 is larger than the 10% Crit Value of -3.038
% which means that there is a less than 90%
% probability that these 2 time series are cointegrated.
% -2.14 的 t 统计量大于 10% 临界值 -3.038
% 这意味着这两个时间序列协整的概率小于 90%。

results=ols(adjcls(:, 1), adjcls(:, 2)); 

hedgeRatio=results.beta
z=results.resid;

% A hedgeRatio of 1.0114 was found. I.e. KO=1.0114*PEP + z, where z can be interpreted as the
% spread KO-1.0114*PEP, which is not stationary here.
% 得到的 hedgeRatio 为 1.0114，即 KO=1.0114*PEP + z，其中 z 可以解释为价差 KO-1.0114*PEP，此处它并非平稳。

plot(z); % This should produce a chart similar to Figure 7.2 (except for the titles and labels).
% 这应该会生成与 Figure 7.2 相似的图形（标题和标签除外）。

% A test for correlation.
% 相关性检验。
dailyReturns=(adjcls-lag1(adjcls))./lag1(adjcls);
[R,P]=corrcoef(dailyReturns(2:end, :));

% R =
% 
%     1.0000    0.4849
%     0.4849    1.0000
% 
% 
% P =
% 
%      1     0
%      0     1

% The P value of 0 indicates that the two time series are significantly
% correlated.
% P 值为 0 表明这两个时间序列显著相关。

