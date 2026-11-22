function y=fwdshift(day,x)
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
% 作者：Ernest Chan
% 著有“Quantitative Trading:
% How to Start Your Own Algorithmic Trading Business”一书

assert(day>=0);


y=[x(day+1:end,:, :); NaN*ones(day,size(x,2), size(x, 3))];
