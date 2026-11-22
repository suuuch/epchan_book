function y = smartstd(x, dim)
%y = smartstd(x, dim)    std along dimension dim, ignoring NaN and Inf 
% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% y = smartstd(x, dim)    沿 dim 维求标准差，忽略 NaN 和 Inf
% 编写者：
% 作者：Ernest Chan
% 著有“Quantitative Trading:
% How to Start Your Own Algorithmic Trading Business”一书

hasData=isfinite(x);

x(~hasData)=0;

y=std(x);

y(all(~hasData, dim))=NaN;
