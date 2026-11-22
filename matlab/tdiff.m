function dmat = tdiff(x,k)
% PURPOSE: produce matrix differences
% -----------------------------------------
% USAGE: dmat = tdiff(x,k)
% where:    x = input matrix (or vector) of length nobs
%           k = lagged difference order
% -----------------------------------------
% NOTE: uses trimr() and lag()
% -----------------------------------------
% RETURNS: dmat = matrix or vector, differenced by k-periods
%                 e.g. x(t) - x(t-k), of length nobs, 
%                 (first k observations are zero)
% -----------------------------------------
% SEE ALSO: trimr() modeled after Gauss trimr function
% -----------------------------------------
% 用途: 生成矩阵差分
% 用法: dmat = tdiff(x,k)
% 其中: x = 长度为 nobs 的输入矩阵（或向量）
% k = 差分的滞后阶数
% 注意: 使用 trimr() 和 lag()
% 返回: dmat = 按 k 期差分后的矩阵或向量
% 例如 x(t) - x(t-k)，长度为 nobs,
% (前 k 个观测值为零)
% 参见: trimr()，仿照 Gauss 的 trimr 函数编写

% written by:
% James P. LeSage, Dept of Economics
% University of Toledo
% 2801 W. Bancroft St,
% Toledo, OH 43606
% jpl@jpl.econ.utoledo.edu
% 编写者:

% error checking on inputs
% 对输入进行错误检查
if (nargin ~= 2)
 error('Wrong # of arguments to tdiff');
end;

[nobs nvar] = size(x);

if ( k == 0)
 dmat = x;

elseif k ==1
    dmat = zeros(nobs,nvar);
 dmat(2:nobs,:) = x(2:nobs,:)-x(1:nobs-1,:);
else
    
% modified by Jushan Bai
% NYU
% 由 Jushan Bai 修改
% 纽约大学 (NYU)
    dmat =zeros(nobs,nvar);
    dmat(k+1:nobs,:) = x(k+1:nobs,:)-x(1:nobs-k,:);
    
 %   tmp = x - lag(x,1);
 %   for ndiff = 2:k;
 %   tmp = tmp - lag(tmp,1);
 %   end;
 %   dmat = tmp;
 % 先用一阶滞后差分 tmp = x - lag(x,1);
 % 对 ndiff = 2:k 进行循环;
 % 逐阶差分 tmp = tmp - lag(tmp,1);
 % 结束;
 % 结果为 dmat = tmp;
end;

