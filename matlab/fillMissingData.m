function [filledPrices]=fillMissingData(prices)
% [filledPrices]=fillMissingData(prices) fill data in a 2-dim array with NaN's with the
% previous value.
% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% 用法：[filledPrices]=fillMissingData(prices)，用前一个值填补
% 二维数组中的 NaN 缺失值。
% 编写者：
% 作者：Ernest Chan
% 著有“Quantitative Trading:
% How to Start Your Own Algorithmic Trading Business”一书

filledPrices=prices;
for t=2:size(filledPrices, 1)
    missData=~isfinite(filledPrices(t, :));
    filledPrices(t, missData)=filledPrices(t-1, missData);
end