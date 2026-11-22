function assert(pred, str)
% ASSERT Raise an error if the predicate is not true.
% assert(pred, string)
%
% written by:
% Ernest Chan
%
% Author of “Quantitative Trading: 
% How to Start Your Own Algorithmic Trading Business”
%
% ernest@epchan.com
% www.epchan.com
% ASSERT 若断言条件不成立，则抛出错误。
% 用法：assert(pred, string)
% 编写者：
% 作者：Ernest Chan
% 著有“Quantitative Trading:
% How to Start Your Own Algorithmic Trading Business”一书

if nargin<2, str = ''; end

if ~pred
  s = sprintf('assertion violated: %s', str);
  error(s);
end
