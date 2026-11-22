function y=backshift(day,x)
% y=backshift(day,x)
% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% 用法：y=backshift(day,x)
% 编写者：
% 作者：Ernest Chan
% 著有?Quantitative Trading:
% How to Start Your Own Algorithmic Trading Business?一书

%assert(day>=0);
% assert(day>=0);（断言 day 大于等于 0）
if day<0 
    error(['day = ' num2str(day) '<0, error!']); 
end 
%y=[NaN(day,size(x,2), size(x, 3));x(1:end-day,:, :)];
% y=[NaN(day,size(x,2), size(x, 3));x(1:end-day,:, :)];（前面补上 day 行 NaN）
tmp1=zeros(day,size(x,2),size(x,3))*NaN;
tmp2=x(1:end-day,:, :);
y=[tmp1;tmp2];