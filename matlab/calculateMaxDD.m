function [maxDD, maxDDD]=calculateMaxDD(cumret)
% [maxDD maxDDD]=calculateMaxDD(cumret)
% calculation of maximum drawdown and maximum drawdown duration based on
% cumulative COMPOUNDED returns. cumret must be a compounded cumulative return.
% Same as calculateMaxDD_cpd for backward compatibility.
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% 用法: [maxDD maxDDD]=calculateMaxDD(cumret)
% 基于累计 COMPOUNDED 收益率计算最大回撤和最大回撤持续时间。cumret 必须是复利累计收益率。
% 为保持向后兼容，与 calculateMaxDD_cpd 相同。
% 编写者:
% 作者: 《Quantitative Trading: How to Start Your Own Algorithmic Trading Business》

highwatermark=zeros(size(cumret)); % initialize high watermarks to zero.
% 将高水位初始化为零。

drawdown=zeros(size(cumret)); % initialize drawdowns to zero.
% 将回撤初始化为零。

drawdownduration=zeros(size(cumret)); % initialize drawdown duration to zero.
% 将回撤持续时间初始化为零。

for t=2:length(cumret)
    highwatermark(t)=max(highwatermark(t-1), cumret(t));
%    drawdown(t)=(1+cumret(t))./(1+highwatermark(t))-1; % drawdown on each day
% 每日回撤
    drawdown(t)=(1+highwatermark(t))/(1+cumret(t))-1; % drawdown on each day
    % 每日回撤
    if (drawdown(t)==0)
        drawdownduration(t)=0;
    else
        drawdownduration(t)=drawdownduration(t-1)+1;
    end
end

maxDD=max(drawdown); % maximum drawdown
% 最大回撤

maxDDD=max(drawdownduration); % maximum drawdown duration
% 最大回撤持续时间
