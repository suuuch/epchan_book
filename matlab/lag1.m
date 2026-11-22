function y=lag(x)
% y=lag(x)
% 
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% 用法：y=lag(x)
% 编写者：
% 作者：Ernest Chan
% 著有“Quantitative Trading:
% How to Start Your Own Algorithmic Trading Business”一书

if (isnumeric(x))
    tmp=[1,size(x,2)];
    tmp(1:1,1:size(x,2))=NaN;
    % y=[NaN(1,size(x,2));x(1:end-1, :)]; % populate the first entry with NaN
    % 将第一个元素填充为 NaN
    y=[tmp;x(1:end-1, :)]; % populate the first entry with NaN
    % 将第一个元素填充为 NaN
elseif (ischar(x))
    y=[repmat('',[1 size(x,2)]);x(1:end-1, :)]; % populate the first entry with ''
    % 将第一个元素填充为 ''
else
    error('Can only be numeric or char array');
end