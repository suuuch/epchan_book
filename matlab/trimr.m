function z = trimr(x,n1,n2)
% PURPOSE: return a matrix (or vector) x stripped of the specified rows.
% -----------------------------------------------------
% USAGE: z = trimr(x,n1,n2)
% where: x = input matrix (or vector) (n x k)
%       n1 = first n1 rows to strip
%       n2 = last  n2 rows to strip
% NOTE: modeled after Gauss trimr function
% -----------------------------------------------------
% RETURNS: z = x(n1+1:n-n2,:)
% -----------------------------------------------------
% 用途: 返回去除指定行后的矩阵（或向量）x
% 用法: z = trimr(x,n1,n2)
% 其中: x = 输入矩阵（或向量）(n x k)
% n1 = 需要去除的前 n1 行
% n2 = 需要去除的后 n2 行
% 注意: 仿照 Gauss 的 trimr 函数编写
% 返回: z = x(n1+1:n-n2,:)

% written by:
% James P. LeSage, Dept of Economics
% University of Toledo
% 2801 W. Bancroft St,
% Toledo, OH 43606
% jpl@jpl.econ.utoledo.edu
% 编写者:

  [n junk] = size(x);
  if (n1+n2) >= n; 
     error('Attempting to trim too much in trimr');
  end;
  h1 = n1+1;   
  h2 = n-n2;
  z = x(h1:h2,:);
  
