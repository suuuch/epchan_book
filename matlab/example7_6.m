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
% 著有《Quantitative Trading: How to Start Your Own Algorithmic Trading Business》一书。

clear;

% Add this folder and the data folder to the MATLAB path.
% 将此文件夹和数据文件夹添加到 MATLAB 路径中。
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);

load('IJR_20080131');
%save('myfile.mat','-v6');
% 保存为 MAT 文件 save('myfile.mat','-v6');

onewaytcost=0.0005; % 5bp one way transaction cost
% 单边交易成本 5bp

%years=year(cellstr(datestr(datenum(cellstr(num2str(tday)), 'yyyymmdd'))));
%months=month(cellstr(datestr(datenum(cellstr(num2str(tday)), 'yyyymmdd'))));
% 提取年份 years=year(cellstr(datestr(datenum(cellstr(num2str(tday)), 'yyyymmdd'))));
% 提取月份 months=month(cellstr(datestr(datenum(cellstr(num2str(tday)), 'yyyymmdd'))));
years=fix(tday/10000);
months=fix(mod(tday,10000)/100);

nextdayyear=fwdshift(1, years);
nextdaymonth=fwdshift(1, months);

lastdayofDec=find(months==12 & nextdaymonth==1);
lastdayofJan=find(months==1 & nextdaymonth==2);

lastdayofJan(1)=[]; % lastdayofDec starts in 2004, so remove 2004 from lastdayofJan
% lastdayofDec 从 2004 年开始，因此从 lastdayofJan 中删除 2004 年
assert(all(tday(lastdayofJan) > tday(lastdayofDec))); % Ensure each lastdayofJan date after each lastdayofDec date
% 确保每个 lastdayofJan 日期都晚于相应的 lastdayofDec 日期

eoy=find(years~=nextdayyear); % End Of Year indices
% 年末索引

eoy(end)=[]; % last index is not End of Year
% 最后一个索引不是年末

assert(all(tday(eoy)==tday(lastdayofDec))); % Ensure eoy dates match lastdayofDec dates
% 确保 eoy 日期与 lastdayofDec 日期一致

annret=(cl(eoy(2:end), :)-cl(eoy(1:end-1), :))./cl(eoy(1:end-1), :); % annual returns
% 年度收益率
janret=(cl(lastdayofJan(2:end), :)-cl(lastdayofDec(2:end), :))./cl(lastdayofDec(2:end), :); % January returns
% 一月收益率

for y=1:size(annret, 1)
    hasData=find(isfinite(annret(y, :))); % pick those stocks with valid annual returns
    % 挑选年度收益率有效的股票
    [foo sortidx]=sort(annret(y, hasData)); % sort stocks based on prior year's returns
    % 按上一年度收益率对股票排序
    
    topN=round(length(hasData)/10); % buy stocks with lowest decile of returns, and vice versa for highest decile
    % 买入收益率最低十分位的股票，对最高十分位则反之
    
    portRet=(smartmean(janret(y, hasData(sortidx(1:topN))))-smartmean(janret(y, hasData(sortidx(end-topN+1:end)))))/2-2*onewaytcost; % portfolio returns
    % 投资组合收益率
    fprintf(1,'Last holding date %i: Portfolio return=%7.4f\n', tday(lastdayofDec(y+1)), portRet);
end
% These should be the output
% Last holding date 20051230: Portfolio return=-0.0244
% Last holding date 20061229: Portfolio return=-0.0068
% Last holding date 20071231: Portfolio return= 0.0881
% 输出结果应如下
% 最后持仓日 20051230: 投资组合收益率=-0.0244
% 最后持仓日 20061229: 投资组合收益率=-0.0068
% 最后持仓日 20071231: 投资组合收益率= 0.0881
