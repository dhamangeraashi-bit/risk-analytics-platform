import numpy as np
import pandas as pd

TRADING_DAYS = 252
RISK_FREE_RATE = 0.05  # 5% annualized assumption, documented here on purpose

def daily_returns(prices: pd.Series) -> pd.Series:
    """Day-over-day percentage change in price."""
    return prices.pct_change().dropna()

def annualized_return(returns: pd.Series) -> float:
    return returns.mean() * TRADING_DAYS

def annualized_volatility(returns: pd.Series) -> float:
    return returns.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(returns: pd.Series) -> float:
    excess = annualized_return(returns) - RISK_FREE_RATE
    vol = annualized_volatility(returns)
    return excess / vol if vol != 0 else float("nan")

def sortino_ratio(returns: pd.Series) -> float:
    downside = returns[returns < 0]
    downside_vol = downside.std() * np.sqrt(TRADING_DAYS)
    excess = annualized_return(returns) - RISK_FREE_RATE
    return excess / downside_vol if downside_vol != 0 else float("nan")

def max_drawdown(prices: pd.Series) -> float:
    cumulative = (1 + daily_returns(prices)).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    return drawdown.min()

def value_at_risk_95(returns: pd.Series) -> float:
    return np.percentile(returns, 5)

def rolling_correlation_matrix(price_df: pd.DataFrame) -> pd.DataFrame:
    """price_df: columns are tickers, values are closing prices, same date index."""
    returns = price_df.pct_change().dropna()
    return returns.corr()