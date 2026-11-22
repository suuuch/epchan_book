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
% 作者 Ernest Chan
% 著有《Quantitative Trading: How to Start Your Own Algorithmic Trading Business》
% 一书。

clear; % make sure previously defined variables are erased.
% 清空之前已定义的变量。

% Add this folder and the data folder to the MATLAB path.
% 将此文件夹和数据文件夹添加到 MATLAB 路径中。
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);

% [num, txt]=xlsread('GLD'); % read a spreadsheet named "GLD.xls" into MATLAB. 
% 将名为 "GLD.xls" 的电子表格读入 MATLAB。

% tday1=txt(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。

% tday1=datestr(datenum(tday1, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将格式转换为 yyyymmdd。

% tday1=str2double(cellstr(tday1)); % convert the date strings first into cell arrays and then into numeric format.
% 先把日期字符串转换为单元格数组，再转换为数值格式。

[tday1, adjcls1]=getTday('GLD');

%adjcls1=num(:, end); % the last column contains the adjusted close prices.
% 最后一列包含调整后的收盘价。

% [num, txt]=xlsread('GDX'); % read a spreadsheet named "GDX.xls" into MATLAB. 
% 将名为 "GDX.xls" 的电子表格读入 MATLAB。

% tday2=txt(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。

% tday2=datestr(datenum(tday2, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将格式转换为 yyyymmdd。

% tday2=str2double(cellstr(tday2)); % convert the date strings first into cell arrays and then into numeric format.
% 先把日期字符串转换为单元格数组，再转换为数值格式。

[tday2, adjcls2]=getTday('GDX');

% adjcls2=num(:, end); % the last column contains the adjusted close prices.
% 最后一列包含调整后的收盘价。

[tday, idx1, idx2]=intersect(tday1, tday2); % find the intersection of the two data sets, and sort them in ascending order
% 求两个数据集的交集，并按升序排序

cl1=adjcls1(idx1); 

cl2=adjcls2(idx2);  

trainset=1:252; % define indices for training set
% 定义训练集的索引

testset=trainset(end)+1:length(tday); % define indices for test set
% 定义测试集的索引

% determines the hedge ratio on the trainset
% 在训练集上确定对冲比率
results=ols(cl1(trainset), cl2(trainset)); % use regression function 
% 使用回归函数
hedgeRatio=results.beta;

spread=cl1-hedgeRatio*cl2; % spread = GLD - hedgeRatio*GDX
% 即 spread = GLD - hedgeRatio*GDX

plot(spread(trainset));

figure;

plot(spread(testset));

figure;

spreadMean=mean(spread(trainset)); % mean  of spread on trainset
% 训练集上价差的均值

spreadStd=std(spread(trainset)); % standard deviation of spread on trainset
% 训练集上价差的标准差

zscore=(spread - spreadMean)./spreadStd; % z-score of spread
% 价差的 z-score

longs=zscore<=-2; % buy spread when its value drops below 2 standard deviations.
% 当价差跌破 2 倍标准差时买入价差。

shorts=zscore>=2; % short spread when its value rises above 2 standard deviations.
% 当价差升破 2 倍标准差时做空价差。

exits=abs(zscore)<=1; % exit any spread position when its value is within 1 standard deviation of its mean.
% 当价差处于其均值 1 倍标准差范围内时，平掉所有价差持仓。

% positions=NaN(length(tday), 2); % initialize positions array
% positions=NaN(length(tday)); % initialize positions array
% 初始化持仓数组
% 初始化持仓数组
positions=[length(tday), 2];
positions(1:length(tday), 1:2)=NaN;

positions(shorts, :)=repmat([-1 1], [length(find(shorts)) 1]); % long entries
% 多头入场

positions(longs,  :)=repmat([1 -1], [length(find(longs)) 1]); % short entries
% 空头入场

positions(exits,  :)=zeros(length(find(exits)), 2); % exit positions
% 平仓

positions=fillMissingData(positions); % ensure existing positions are carried forward unless there is an exit signal
% 确保在没有平仓信号时原有持仓被延续下来

cl=[cl1 cl2]; % combine the 2 price series
% 合并两条价格序列

dailyret=(cl - lag1(cl))./lag1(cl);

pnl=sum(lag1(positions).*dailyret, 2);

sharpeTrainset=sqrt(252)*mean(pnl(trainset(2:end)))./std(pnl(trainset(2:end))) % the Sharpe ratio on the training set should be about 2.3
% 训练集上的夏普比率应约为 2.3

sharpeTestset=sqrt(252)*mean(pnl(testset))./std(pnl(testset)) % the Sharpe ratio on the test set should be about 1.5
% 测试集上的夏普比率应约为 1.5

plot(cumsum(pnl(testset)));

save(fullfile(dataDir, 'example3_6_positions'), 'positions'); % save positions file for checking look-ahead bias.
% 保存持仓文件以检查前视偏差。



