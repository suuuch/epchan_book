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

[num, txt]=xlsread('IGE'); % read a spreadsheet named "IGE.xls" into MATLAB. 
% 将名为 "IGE.xls" 的电子表格读入 MATLAB。

tday=num(1:end, 1);

tday=datestr(tday+datenum('30-Dec-1899'), 'yyyymmddTHHMMSS');

len=length(tday);
tdaycell = cell(len, 1);
for k=1:1:len
    tdaycell{k,1} = tday(k, 1:8);
end

% tday=str2double(cellstr(tday)); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，然后再转换为数值格式。
tday=str2double(tdaycell); % convert the date strings first into cell arrays and then into numeric format.
% 先将日期字符串转换为单元格数组，然后再转换为数值格式。

cls=num(:, end); % the last column contains the adjusted close prices.
% 最后一列包含复权收盘价。

[tday sortIndex]=sort(tday); % sort tday into ascending order.
% 将 tday 按升序排序。

cls=cls(sortIndex); % sort cls into ascending order of dates.
% 按日期升序排列 cls。

dailyret=(cls(2:end)-cls(1:end-1))./cls(1:end-1); % daily returns
% 每日收益率

excessRet=dailyret - 0.04/252; % excess daily returns = strategy returns - financing cost, assuming risk-free rate of 4% per annum and 252 trading days in a year
% 超额每日收益率 = 策略收益率 - 融资成本，假设年化无风险利率为 4%，一年有 252 个交易日

sharpeRatio=sqrt(252)*mean(excessRet)/std(excessRet) % the output should be 0.7893
% 输出结果应为 0.7893