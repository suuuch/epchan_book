function y = smartmean(x,dim)
%SMARTMEAN   Average or mean value ignoring NaN.
%
%   Same as MEAN except that it returns the mean of the finite elements
%   instead of propagating NaN and Inf
%   Returns NaN if there are no finite elements
%
%   For vectors, MEAN(X) is the mean value of the elements in X. For
%   matrices, MEAN(X) is a row vector containing the mean value of
%   each column.  For N-D arrays, MEAN(X) is the mean value of the
%   elements along the first non-singleton dimension of X.
%
%   MEAN(X,DIM) takes the mean along the dimension DIM of X. 
%
%   Example: If X = [0 1 2
%                    3 4 5]
%
%   then mean(X,1) is [1.5 2.5 3.5] and mean(X,2) is [1
%                                                     4]
%
%   See also MEDIAN, STD, MIN, MAX, COV.
% SMARTMEAN   忽略 NaN 的平均值或均值。
% 与 MEAN 相同，但它返回有限元素的均值，而不是传播 NaN 和 Inf
% 若不存在有限元素则返回 NaN
% 对向量，MEAN(X) 是 X 中各元素的均值。对矩阵，MEAN(X) 是包含各列均值的行向量。对于 N 维数组，MEAN(X) 是沿 X 第一个非单例维度的元素均值。
% MEAN(X,DIM) 沿 X 的 DIM 维度求均值。
% 例如: 若 X = [0 1 2
% 则 mean(X,1) 为 [1.5 2.5 3.5], mean(X,2) 为 [1
% 参见 MEDIAN, STD, MIN, MAX, COV.

%   Copyright (c) 1984-98 by The MathWorks, Inc.
%   $Revision: 5.13 $  $Date: 1997/11/21 23:23:55 $
% 版权所有 (c) 1984-98 The MathWorks, Inc.
% 修订: $Revision: 5.13 $  日期: $Date: 1997/11/21 23:23:55 $

if nargin==1, 
  % Determine which dimension SUM will use
  % 确定 SUM 将使用的维度
  dim = min(find(size(x)~=1));
  if isempty(dim), dim = 1; end
  k=isfinite(x);
  x(~k)=0;
  warning off
  y=sum(x)./sum(k,dim);
  y(all(~isfinite(x)))=NaN;
  warning on
else
  k=isfinite(x);
  x(~k)=0;
  warning off
  y=sum(x,dim)./sum(k,dim);
  y(all(~isfinite(x), dim))=NaN;
  warning on
end
