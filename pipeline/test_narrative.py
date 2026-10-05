from narrative import generate_narrative

fake_metrics = {
    "annualized_return": 0.6119,
    "annualized_volatility": 0.2748,
    "sharpe_ratio": 2.04,
    "sortino_ratio": 2.67,
    "max_drawdown": -0.1271,
    "var_95": -0.0202,
}

note = generate_narrative("AAPL", fake_metrics)
print(note)