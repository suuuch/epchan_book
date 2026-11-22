function y = smartmean(x, dim)
% y = smartmean(x, dim)   Mean value along dimension dim, ignoring NaN. 
%
% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% y = smartmean(x, dim)   沿 dim 维求均值，忽略 NaN。
% 编写者：
% 作者：Ernest Chan
% 著有“Quantitative Trading:
% How to Start Your Own Algorithmic Trading Business”一书

hasData=isfinite(x);
x(~hasData)=0;
y=sum(x,dim)./sum(hasData, dim);
y(all(~hasData, dim))=NaN; % set y to NaN if all entries are NaN's.
% 如果所有元素都是 NaN，则将 y 设为 NaN。

