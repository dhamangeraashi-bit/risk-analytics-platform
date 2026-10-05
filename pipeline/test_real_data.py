import sys
sys.path.append("../mcp_servers")

import yfinance as yf
from market_metrics import (
    daily_returns, annualized_return, annualized_volatility,
    sharpe_ratio, sortino_ratio, max_drawdown, value_at_risk_95
)

tickers = ["AAPL", "MSFT", "NVDA"]

for ticker in tickers:
    data = yf.Ticker(ticker).history(period="6mo")
    prices = data["Close"]
    returns = daily_returns(prices)

    print(f"\n--- {ticker} (6-month) ---")
    print(f"Annualized return:     {annualized_return(returns):.2%}")
    print(f"Annualized volatility: {annualized_volatility(returns):.2%}")
    print(f"Sharpe ratio:          {sharpe_ratio(returns):.2f}")
    print(f"Sortino ratio:         {sortino_ratio(returns):.2f}")
    print(f"Max drawdown:          {max_drawdown(prices):.2%}")
    print(f"95% VaR (daily):       {value_at_risk_95(returns):.2%}")

import pandas as pd
from market_metrics import rolling_correlation_matrix

price_data = {}
for ticker in tickers:
    price_data[ticker] = yf.Ticker(ticker).history(period="6mo")["Close"]

price_df = pd.DataFrame(price_data)
corr = rolling_correlation_matrix(price_df)
print("\nRow counts:", {t: len(price_data[t]) for t in tickers})
print("Any missing dates?\n", price_df.isna().sum())
print("\n--- Correlation Matrix ---")
print(corr.round(2))