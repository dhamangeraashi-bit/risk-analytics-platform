import pandas as pd
from market_metrics import daily_returns, sharpe_ratio, sortino_ratio, max_drawdown, value_at_risk_95, annualized_volatility

prices = pd.Series([100, 102, 101, 105, 104])
returns = daily_returns(prices)

print("Daily returns:\n", returns)
print("\nAnnualized volatility:", annualized_volatility(returns))
print("Sharpe ratio:", sharpe_ratio(returns))
print("Sortino ratio:", sortino_ratio(returns))
print("Max drawdown:", max_drawdown(prices))
print("95% VaR:", value_at_risk_95(returns))