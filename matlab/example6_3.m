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
% 作者: ?Quantitative Trading: How to Start Your Own Algorithmic Trading Business?

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
 
% [num1, txt1]=xlsread('OIH'); % read a spreadsheet named "OIH.xls" into MATLAB. 
% 将名为 "OIH.xls" 的电子表格读入 MATLAB。
 
% tday1=txt1(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。
 
% tday1=datestr(datenum(tday1, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将格式转换为 yyyymmdd。
 
% tday1=str2double(cellstr(tday1)); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，然后再转换为数值格式。
 
% adjcls1=num1(:, end); % the last column contains the adjusted close prices.
% 最后一列包含复权后收盘价。
[tday1, adjcls1]=getTday('OIH');

% [num2, txt2]=xlsread('RKH'); % read a spreadsheet named "RKH.xls" into MATLAB. 
% 将名为 "RKH.xls" 的电子表格读入 MATLAB。
 
% tday2=txt2(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。
 
% tday2=datestr(datenum(tday2, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将格式转换为 yyyymmdd。
 
% tday2=str2double(cellstr(tday2)); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，然后再转换为数值格式。

% adjcls2=num2(:, end);
% 复权后收盘价: adjcls2=num2(:, end);
[tday2, adjcls2]=getTday('RKH');

% [num3, txt3]=xlsread('RTH'); % read a spreadsheet named "RTH.xls" into MATLAB. 
% 将名为 "RTH.xls" 的电子表格读入 MATLAB。
 
% tday3=txt3(2:end, 1); % the first column (starting from the second row) is the trading days in format mm/dd/yyyy.
% 第一列（从第二行开始）是 mm/dd/yyyy 格式的交易日。
 
% tday3=datestr(datenum(tday3, 'mm/dd/yyyy'), 'yyyymmdd'); % convert the format into yyyymmdd.
% 将格式转换为 yyyymmdd。
 
% tday3=str2double(cellstr(tday3)); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，然后再转换为数值格式。

% adjcls3=num3(:, end);
% 复权后收盘价: adjcls3=num3(:, end);
[tday3, adjcls3]=getTday('RTH');

% merge these data
% 合并这些数据
tday=union(tday1, tday2);
tday=union(tday, tday3);
% adjcls=NaN(length(tday), 3);
% 复权后收盘价矩阵: adjcls=NaN(length(tday), 3);
tmp=[length(tday), 3];
tmp(1:length(tday),1:3)=NaN;
adjcls=tmp;

[foo idx1 idx]=intersect(tday1, tday);
adjcls(idx, 1)=adjcls1(idx1);
[foo idx2 idx]=intersect(tday2, tday);
adjcls(idx, 2)=adjcls2(idx2);
[foo idx3 idx]=intersect(tday3, tday);
adjcls(idx, 3)=adjcls3(idx3);

ret=(adjcls-lag1(adjcls))./lag1(adjcls); % returns
% 收益率

baddata=find(any(~isfinite(ret), 2)); % days where any one return is missing
% 任一收益率缺失的交易日

ret(baddata, :)=[]; % eliminate days where any one return is missing
% 剔除任一收益率缺失的交易日

excessRet=ret-repmat(0.04/252, size(ret)); % excess returns: assume annualized risk free rate is 4%
% 超额收益率：假设年化无风险利率为 4%

M=252*mean(excessRet, 1)' % annualized mean excess returns
% 年化平均超额收益率
% M =
% 
%     0.1396
%     0.0294
%    -0.0073

C=252*cov(excessRet) % annualized covariance matrix
% 年化协方差矩阵
% C =
% 
%     0.1109    0.0200    0.0183
%     0.0200    0.0372    0.0269
%     0.0183    0.0269    0.0420

F=inv(C)*M % Kelly optimal leverages
% Kelly 最优杠杆
% F =
% 
%     1.2919
%     1.1723
%    -1.4882

g=0.04+F'*C*F/2 % Maximum annualized compounded growth rate
% 最大年化复合增长率
% g =
% 
%     0.1529

S=sqrt(F'*C*F) % Sharpe ratio of portfolio
% 投资组合的夏普比率
% S =
% 
%     0.4751