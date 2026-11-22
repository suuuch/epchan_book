clear;

% Add this folder and the data folder to the MATLAB path.
% 将本文件夹和数据文件夹添加到 MATLAB 路径中。
thisDir=fileparts(which(mfilename));
if isempty(thisDir), thisDir=pwd; end
addpath(thisDir);
dataDir=fullfile(thisDir, '..', 'data');
if ~exist(dataDir, 'dir'), dataDir=fullfile(thisDir, '..', '..', 'data'); end
addpath(dataDir);

lookback=252; % use lookback days as estimation (training) period for determining factor exposures.
% 使用 lookback 天作为估计（训练）期，以确定因子暴露。
numFactors=5;
topN=50; % for trading strategy, long stocks with topN expected 1-day returns.
% 对于交易策略，做多预期 1 日收益率最高的 topN 只股票。

load('IJR_20080114'); % test on SP600 smallcap stocks. (This MATLAB binary input file contains tday, stocks, op, hi, lo, cl arrays.
% 在 SP600 小盘股上测试。（该 MATLAB 二进制输入文件包含 tday、stocks、op、hi、lo、cl 数组。
% save('myfile.mat','-v6');
% 保存数据: save('myfile.mat','-v6');

mycls=fillMissingData(cl);

positionsTable=zeros(size(cl));

dailyret=(mycls-lag1(mycls))./lag1(mycls); % note the rows of dailyret are the observations at different time periods
% 注意 dailyret 的行对应不同时期的观测值

for t=lookback+1:length(tday)

    R=dailyret(t-lookback+1:t,:)'; % here the columns of R are the different observations.
    % 此处 R 的列对应不同的观测值。
    
    hasData=find(all(isfinite(R), 2)); % avoid any stocks with missing returns
    % 剔除收益率有缺失的股票
    
    R=R(hasData, :);
    
    avgR=smartmean(R, 2);
    R=R-repmat(avgR, [1 size(R, 2)]); % subtract mean from returns
    % 从收益率中减去均值
    
    covR=smartcov(R'); % compute covariance matrix, with observations in rows.
    % 计算协方差矩阵，观测值按行排列。
    
    [X, B]=eig(covR); % X is the factor exposures matrix, B the variances of factor returns
    % X 是因子暴露矩阵，B 是因子收益率的方差
    
    X(:, 1:size(X, 2)-numFactors)=[]; % Retain only numFactors
    % 只保留 numFactors
    
    results=ols(R(:, end), X); % b are the factor returns for time period t-1 to t.
    % b 是 t-1 到 t 期的因子收益率。
    b=results.beta;
    
    Rexp=avgR+X*b; % Rexp is the expected return for next period assuming factor returns remain constant.
    % Rexp 是假设因子收益率保持不变时下一期的预期收益率。
    
    [foo idxSort]=sort(Rexp);
    
    positionsTable(t, hasData(idxSort(1:topN)))=-1; % short topN stocks with lowest expected returns
    % 做空预期收益率最低的 topN 只股票
    positionsTable(t, hasData(idxSort(end-topN+1:end)))=1; % buy topN stocks with highest  expected returns
    % 买入预期收益率最高的 topN 只股票
    % hasData(idxSort(end-topN+1:end))=1;
    % 设置持仓为 1: hasData(idxSort(end-topN+1:end))=1;
end

ret=smartsum(backshift(1, positionsTable).*dailyret, 2); % compute daily returns of trading strategy
% 计算交易策略的每日收益率
avgret=smartmean(ret)*252 % compute annualized average return of trading strategy
% 计算交易策略的年化平均收益率
% A very poor return!
% avgret =
% 
%    -1.8099
% 非常差的收益率！
% 平均收益率 avgret =