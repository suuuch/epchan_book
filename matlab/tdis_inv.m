function x = tdis_inv (p, a)
% PURPOSE: returns the inverse (quantile) at x of the t(n) distribution
%---------------------------------------------------
% USAGE: x = tdis_inv(p,n)
% where: p = a vector of probabilities 
%        n = a scalar dof parameter
%---------------------------------------------------
% RETURNS:
%        a vector of tinv at each element of x of the t(n) distribution      
% --------------------------------------------------
% SEE ALSO: tdis_cdf, tdis_rnd, tdis_pdf, tdis_prb
%---------------------------------------------------
% 用途: 返回 t(n) 分布在 x 处的反函数（分位数）
% 用法: x = tdis_inv(p,n)
% 其中: p = 概率向量
% n = 标量自由度参数
% 返回:
% t(n) 分布在 x 各元素处的 tinv 值向量
% 参见: tdis_cdf, tdis_rnd, tdis_pdf, tdis_prb

%       Anders Holtsberg, 18-11-93
%       Copyright (c) Anders Holtsberg
% 版权所有 (c) Anders Holtsberg
   

  if (nargin ~= 2)
    error ('Wrong # of arguments to tdis_inv');
  end

s = p<0.5; 
p = p + (1-2*p).*s;
p = 1-(2*(1-p));
x = beta_inv(p,1/2,a/2);
x = x.*a./((1-x));
x = (1-2*s).*sqrt(x);
