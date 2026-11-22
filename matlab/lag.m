function z = lag(x,n,v)
% PURPOSE: creates a matrix or vector of lagged values
% -------------------------------------------------------
% USAGE: z = lag(x,n,v)
% where: x = input matrix or vector, (nobs x k)
%        n = order of lag
%        v = (optional) initial values (default=0)
% e.g.
%     z = lag(x) creates a matrix (or vector) of x, lagged 1 observations
%     z = lag(x,n) creates a matrix (or vector) of x, lagged n observations
%     z = lag(x,n,v) creates a matrix (or vector) of x, lagged n observations,
%         with initial values taking a value v.
% ------------------------------------------------------
% RETURNS: z = matrix (or vector) of lags (nobs x k)
% ------------------------------------------------------
% NOTES: if n <= 0, z = [] is returned. While you may find this
%        preverse, it is sometimes useful.
%-------------------------------------------------------
% SEE ALSO: mlag() 
%-------------------------------------------------------
% 用途: 创建滞后值的矩阵或向量
% 用法: z = lag(x,n,v)
% 其中: x = 输入矩阵或向量, (nobs x k)
% n = 滞后的阶数
% v = (可选) 初始值 (默认值=0)
% 例如:
% z = lag(x) 创建 x 滞后 1 个观测值的矩阵 (或向量)
% z = lag(x,n) 创建 x 滞后 n 个观测值的矩阵 (或向量)
% z = lag(x,n,v) 创建 x 滞后 n 个观测值的矩阵 (或向量), 初始值取 v。
% 返回: z = 滞后值的矩阵 (或向量) (nobs x k)
% 注意: 如果 n <= 0, 将返回 z = []。虽然你可能觉得这样做很荒谬, 但有时还是很有用的。
% 参见: mlag()

% written by:
% James P. LeSage, Dept of Economics
% University of Toledo
% 2801 W. Bancroft St,
% Toledo, OH 43606
% jpl@jpl.econ.utoledo.edu
% 编写者:

switch(nargin)

case 1
   n = 1; v = 0;
   zt = ones(n,cols(x))*v;
   z = [ zt; trimr(x,0,n)];

case 2
   v = 0;
   if n < 1
   z = [];
   else
   zt = ones(n,cols(x))*v;
   z = [ zt; trimr(x,0,n)];
   end

case 3
   if n < 1
   z = [];
   else
   zt = ones(n,cols(x))*v;
   z = [ zt; trimr(x,0,n)];
   end

otherwise
error('lag: wrong # of input arguments');
end;

  
