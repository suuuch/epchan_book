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

symbol='IBM'; % the stock of interest
% 关注的股票

historicalPriceFile =urlread(['http://finance.yahoo.com/q/hp?s=', symbol]); % retrieving a webpage
% 获取网页

dateField=regexp(historicalPriceFile, '<td class="yfnc_tabledata1" nowrap align="right">([\d\w-]+)</td>', 'tokens'); % extracting the date field to a cell array of cells
% 将日期字段提取到单元格数组中

numField=regexp(historicalPriceFile, '<td class="yfnc_tabledata1" align="right">([\d\.,]+)</td>', 'tokens'); % extracting the numbers field to a cell array of cells
% 将数字字段提取到单元格数组中

dates=[dateField{:}]'; % convert to cell array of strings
% 转换为字符串单元格数组

numField=[numField{:}]'; % convert to cell array of strings
% 转换为字符串单元格数组

% convert to doubles array
% 转换为双精度数组
op=str2double(numField (1:6:end)); % open
% 开盘价
hi=str2double(numField (2:6:end)); % high
% 最高价
lo=str2double(numField (3:6:end)); % low
% 最低价
cl=str2double(numField (4:6:end)); % close
% 收盘价
vol=str2double(numField (5:6:end)); % volume
% 成交量
adjCl=str2double(numField (6:6:end)); % adjusted close
% 复权收盘价
