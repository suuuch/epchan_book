function y = smartstd(x,dim)
%SMARTSTD    Standard deviation of finite elements.
%
%   Same as STD except that it ignores NaN and Inf instead of 
%   propagating them
%
%   Normalizes by N, not N-1
% SMARTSTD    有限元素的标准差。
% 与 STD 相同，但它会忽略 NaN 和 Inf，而不是传播它们
% 按 N 归一化，而不是 N-1

if nargin<2, 
  dim = min(find(size(x)~=1));
  if isempty(dim), dim = 1; end
end

tile=ones(1,max(ndims(x),dim));
tile(dim)=size(x,dim);

xc=x-repmat(smartmean(x,dim),tile);  % Remove mean
% 去除均值
y=sqrt(smartmean(conj(xc).*xc,dim)); % normalize by N
% 按 N 归一化

% y=sqrt(smartsum(conj(xc).*xc,dim)/(smartsum(abs(sign(xc)), dim)-1)); %normalize by N-1
% 按 N-1 归一化
