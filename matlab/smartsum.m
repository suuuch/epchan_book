function y = smartsum(x, dim)
%y = smartsum(x, dim)   Sum along dimension dim, ignoring NaN.
% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% y = smartsum(x, dim)   沿 dim 维求和，忽略 NaN。
% 编写者：
% 作者：Ernest Chan
% 著有“Quantitative Trading:
% How to Start Your Own Algorithmic Trading Business”一书



hasData=isfinite(x);
x(~hasData)=0;
y=sum(x,dim);
y(all(~hasData, dim))=NaN;
