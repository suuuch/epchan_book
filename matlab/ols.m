function results=ols(y,x)
% PURPOSE: least-squares regression 
%---------------------------------------------------
% USAGE: results = ols(y,x)
% where: y = dependent variable vector    (nobs x 1)
%        x = independent variables matrix (nobs x nvar)
%---------------------------------------------------
% RETURNS: a structure
%        results.meth  = 'ols'
%        results.beta  = bhat     (nvar x 1)
%        results.tstat = t-stats  (nvar x 1)
%        results.bstd  = std deviations for bhat (nvar x 1)
%        results.yhat  = yhat     (nobs x 1)
%        results.resid = residuals (nobs x 1)
%        results.sige  = e'*e/(n-k)   scalar
%        results.rsqr  = rsquared     scalar
%        results.rbar  = rbar-squared scalar
%        results.dw    = Durbin-Watson Statistic
%        results.nobs  = nobs
%        results.nvar  = nvars
%        results.y     = y data vector (nobs x 1)
%        results.bint  = (nvar x2 ) vector with 95% confidence intervals on beta
%---------------------------------------------------
% SEE ALSO: prt(results), plt(results)
%---------------------------------------------------
% 用途: 最小二乘回归
% 用法: results = ols(y,x)
% 其中: y = 因变量向量    (nobs x 1)
% x = 自变量矩阵 (nobs x nvar)
% 返回: 一个结构体
% results.meth  = 'ols'，表示估计方法
% results.beta  = bhat     (nvar x 1)，回归系数
% results.tstat = t-stats  (nvar x 1)，t 统计量
% results.bstd  = bhat 的标准差 (nvar x 1)
% results.yhat  = yhat     (nobs x 1)，拟合值
% results.resid = residuals (nobs x 1)，残差
% results.sige  = e'*e/(n-k)   标量，残差方差
% results.rsqr  = rsquared     标量，R 平方
% results.rbar  = rbar-squared 标量，调整后的 R 平方
% results.dw    = Durbin-Watson 统计量
% results.nobs  = nobs，观测值个数
% results.nvar  = nvars，自变量个数
% results.y     = y 数据向量 (nobs x 1)
% results.bint  = (nvar x 2) 向量，包含 beta 的 95% 置信区间
% 参见: prt(results), plt(results)

% written by:
% James P. LeSage, Dept of Economics
% University of Toledo
% 2801 W. Bancroft St,
% Toledo, OH 43606
% jlesage@spatial-econometrics.com
%
% Barry Dillon (CICG Equity)
% added the 95% confidence intervals on bhat
% 编写者:
% Barry Dillon (CICG Equity)：增加了 bhat 的 95% 置信区间

if (nargin ~= 2); error('Wrong # of arguments to ols'); 
else
 [nobs nvar] = size(x); [nobs2 junk] = size(y);
 if (nobs ~= nobs2); error('x and y must have same # obs in ols'); 
 end;
end;

results.meth = 'ols';
results.y = y;
results.nobs = nobs;
results.nvar = nvar;

if nobs < 10000
  [q r] = qr(x,0);
  xpxi = (r'*r)\eye(nvar);
else % use Cholesky for very large problems
% 对非常大的问题使用 Cholesky 分解
  xpxi = (x'*x)\eye(nvar);
end;

results.beta = xpxi*(x'*y);
results.yhat = x*results.beta;
results.resid = y - results.yhat;
sigu = results.resid'*results.resid;
results.sige = sigu/(nobs-nvar);
tmp = (results.sige)*(diag(xpxi));
sigb=sqrt(tmp);
results.bstd = sigb;
tcrit=-tdis_inv(.025,nobs);
results.bint=[results.beta-tcrit.*sigb, results.beta+tcrit.*sigb];
results.tstat = results.beta./(sqrt(tmp));
ym = y - mean(y);
rsqr1 = sigu;
rsqr2 = ym'*ym;
results.rsqr = 1.0 - rsqr1/rsqr2; % r-squared
% R 平方
rsqr1 = rsqr1/(nobs-nvar);
rsqr2 = rsqr2/(nobs-1.0);
if rsqr2 ~= 0
results.rbar = 1 - (rsqr1/rsqr2); % rbar-squared
% 调整后的 R 平方
else
    results.rbar = results.rsqr;
end;
ediff = results.resid(2:nobs) - results.resid(1:nobs-1);
results.dw = (ediff'*ediff)/sigu; % durbin-watson
% Durbin-Watson 统计量
