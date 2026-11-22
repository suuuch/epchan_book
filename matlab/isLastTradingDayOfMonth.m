function isLastTradingDayOfMonth=isLastTradingDayOfMonth(tday)
% isLastTradingDayOfMonth=isLastTradingDayOfMonth(tday) returns a logical
% array. True if tday(t) is last trading day of month.
% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% isLastTradingDayOfMonth=isLastTradingDayOfMonth(tday) 返回一个逻辑数组。若 tday(t) 是该月最后一个交易日，则为真。
% 编写者:
% 作者 Ernest Chan
% 著有《Quantitative Trading: How to Start Your Own Algorithmic Trading Business?》一书。

%tdayStr=datestr(datenum(num2str(tday), 'yyyymmdd'));
% tdayStr=datestr(datenum(num2str(tday), 'yyyymmdd'));（已注释掉的语句）

%todayMonth=month(tdayStr);
% todayMonth=month(tdayStr);（已注释掉的语句）
todayMonth=fix(mod(tday,10000)/100);

tmrMonth=fwdshift(1, todayMonth); % tomorrow's month
% 下一个月的月份

isLastTradingDayOfMonth=false(size(tday));

isLastTradingDayOfMonth(todayMonth~=tmrMonth & isfinite(todayMonth) & isfinite(tmrMonth))=true;
