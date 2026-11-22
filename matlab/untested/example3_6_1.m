% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% 编写者：
% 《Quantitative Trading: How to Start Your Own Algorithmic Trading Business》一书的作者

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

[num, txt]=xlsread('GLD'); % read a spreadsheet named "GLD.xls" into MATLAB. 
% 将名为 "GLD.xls" 的电子表格读入 MATLAB。

tday1=txt(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是格式为 mm/dd/yyyy 的交易日。

tday1=datestr(datenum(tday1, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将日期格式转换为 yyyymmdd。

tday1=str2double(cellstr(tday1)); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，再转换为数值格式。

adjcls1=num(:, end); % the last column contains the adjusted close prices.
% 最后一列包含复权收盘价。

[num, txt]=xlsread('GDX'); % read a spreadsheet named "GDX.xls" into MATLAB. 
% 将名为 "GDX.xls" 的电子表格读入 MATLAB。

tday2=txt(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是格式为 mm/dd/yyyy 的交易日。

tday2=datestr(datenum(tday2, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将日期格式转换为 yyyymmdd。

tday2=str2double(cellstr(tday2)); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，再转换为数值格式。

adjcls2=num(:, end); % the last column contains the adjusted close prices.
% 最后一列包含复权收盘价。

[tday, idx1, idx2]=intersect(tday1, tday2); % find the intersection of the two data sets, and sort them in ascending order
% 求两个数据集的交集，并按升序排列

cl1=adjcls1(idx1); 

cl2=adjcls2(idx2);  

% step one of look-forward bias check
% 前视偏差检验第一步
cutoff=60; % number of most recent trading days to cut off 
% 要截断的最近交易日数量
tday(end-cutoff+1:end, :)=[]; % remove the last cutoff number of days.
% 删除最后 cutoff 天的数据。
cl1(end-cutoff+1:end, :)=[];
cl2(end-cutoff+1:end, :)=[];

trainset=1:252; % define indices for training set
% 定义训练集的索引

testset=trainset(end)+1:length(tday); % define indices for test set
% 定义测试集的索引

vnames=strvcat('GLD', 'GDX');

% test for cointegration of GLD and GDX in the trainset.
% 检验 GLD 与 GDX 在训练集中的协整性。
res=cadf(cl1(trainset), cl2(trainset), 0, 1);

prt(res, vnames);

% determines the hedge ratio on the trainset
% 在训练集上确定对冲比率
results=ols(cl1(trainset), cl2(trainset)); % use regression function 
% 使用回归函数
hedgeRatio=results.beta;

spread=cl1-hedgeRatio*cl2; % spread = GLD - hedgeRatio*GDX
% 价差 spread = GLD - hedgeRatio*GDX

plot(spread(trainset));

figure;

plot(spread(testset));

figure;

spreadMean=mean(spread(trainset)); % mean  of spread on trainset
% 训练集上 spread 的均值

spreadStd=std(spread(trainset)); % standard deviation of spread on trainset
% 训练集上 spread 的标准差

zscore=(spread - spreadMean)./spreadStd; % z-score of spread
% spread 的 z 分数

longs=zscore<=-2; % buy spread when its value drops below 2 standard deviations.
% 当 spread 的值跌至 2 个标准差以下时买入 spread。

shorts=zscore>=2; % short spread when its value rises above 2 standard deviations.
% 当 spread 的值升至 2 个标准差以上时做空 spread。

exits=abs(zscore)<=1; % exit any spread position when its value is within 1 standard deviation of its mean.
% 当 spread 的值回到其均值 1 个标准差以内时平掉所有 spread 持仓。

positions=NaN(length(tday), 2); % initialize positions array
% 初始化 positions 数组

positions(shorts, :)=repmat([-1 1], [length(find(shorts)) 1]); % long entries
% 多头入场

positions(longs,  :)=repmat([1 -1], [length(find(longs)) 1]); % short entries
% 空头入场

positions(exits,  :)=zeros(length(find(exits)), 2); % exit positions
% 平仓

positions=fillMissingData(positions); % ensure existing positions are carried forward unless there is an exit signal
% 确保在没有平仓信号时沿用原有持仓

cl=[cl1 cl2]; % combine the 2 price series
% 合并两条价格序列

dailyret=(cl - lag1(cl))./lag1(cl);

pnl=sum(lag1(positions).*dailyret, 2);

sharpeTrainset=sqrt(252)*mean(pnl(trainset(2:end)))./std(pnl(trainset(2:end))) % the Sharpe ratio on the training set should be about 2.9
% 训练集上的夏普比率应约为 2.9

sharpeTestset=sqrt(252)*mean(pnl(testset))./std(pnl(testset)) % the Sharpe ratio on the test set should be about 1.0
% 测试集上的夏普比率应约为 1.0

plot(cumsum(pnl(testset)));

% step two of look-forward-bias check
% 前视偏差检验第二步
oldoutput=load(fullfile(dataDir, 'example3_6_positions'));
oldoutput.positions(end-cutoff+1:end, :)=[];
 
if (any(positions~=oldoutput.positions))
    fprintf(1, 'Program has look-forward-bias!\n');
end



