function y = smartcov(x)
% Covariance n of finite elements.
% Rows of observations, columns of variables
%   Same as COV except that it ignores NaN and Inf instead of 
%   propagating them
%
%   Normalizes by N, not N-1
% 有限元素的协方差。
% 观测值为行，变量为列
% 与 COV 相同，但它会忽略 NaN 和 Inf，而不是传播它们
% 按 N 归一化，而不是 N-1

% y=NaN(size(x, 2), size(x, 2));
% y=NaN(size(x, 2), size(x, 2));（初始化输出矩阵）
tmp=[size(x, 2), size(x, 2)];
tmp(1:size(x, 2),1:size(x, 2))=NaN;
y=tmp;
% xc=NaN(size(x));
% xc=NaN(size(x));（初始化去均值前的数组）
tmp=[size(x), size(x)];
tmp(1:size(x),1:size(x))=NaN;
xc=tmp;

goodstk=find(~all(isnan(x), 1));

xc(:, goodstk)=x(:, goodstk)-repmat(smartmean(x(:, goodstk),1), [size(x, 1) 1]);  % Remove mean
% 去除均值

for m=1:length(goodstk)
    for n=m:length(goodstk)
        y(goodstk(m), goodstk(n))=smartmean(xc(:, goodstk(m)).*xc(:, goodstk(n)), 1);
        y(goodstk(n), goodstk(m))=y(goodstk(m), goodstk(n));
    end
end