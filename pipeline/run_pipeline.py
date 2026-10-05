from obsidian_writer.write_notes import write_narrative_note
from narrative import generate_narrative
import sqlite3
import yfinance as yf
from datetime import date
from market_metrics import (
    daily_returns, annualized_return, annualized_volatility,
    sharpe_ratio, sortino_ratio, max_drawdown, value_at_risk_95,
    rolling_correlation_matrix
)
import pandas as pd

DB_PATH = "../data/analytics.db"
TICKERS = ["AAPL", "MSFT", "NVDA"]

def init_db(conn):
    with open("schema.sql") as f:
        conn.executescript(f.read())

def run():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    today = date.today().isoformat()

    price_data = {}
    for ticker in TICKERS:
        hist = yf.Ticker(ticker).history(period="6mo")
        prices = hist["Close"]
        price_data[ticker] = prices
        returns = daily_returns(prices)

        conn.execute("INSERT OR IGNORE INTO securities (ticker, name) VALUES (?, ?)", (ticker, ticker))

        for dt, close in prices.items():
            conn.execute(
                "INSERT OR REPLACE INTO prices (ticker, date, close) VALUES (?, ?, ?)",
                (ticker, dt.strftime("%Y-%m-%d"), float(close))
            )

        conn.execute("""
            INSERT OR REPLACE INTO risk_metrics
            (ticker, as_of_date, annualized_return, annualized_volatility, sharpe_ratio, sortino_ratio, max_drawdown, var_95)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticker, today,
            annualized_return(returns), annualized_volatility(returns),
            sharpe_ratio(returns), sortino_ratio(returns),
            max_drawdown(prices), value_at_risk_95(returns)
        ))
        print(f"Saved {ticker} metrics for {today}")
        metrics_dict = {
            "annualized_return": annualized_return(returns),
            "annualized_volatility": annualized_volatility(returns),
            "sharpe_ratio": sharpe_ratio(returns),
            "sortino_ratio": sortino_ratio(returns),
            "max_drawdown": max_drawdown(prices),
            "var_95": value_at_risk_95(returns),
        }
        note = generate_narrative(ticker, metrics_dict)
        conn.execute(
            "INSERT INTO narratives (scope, as_of_date, summary) VALUES (?, ?, ?)",
            ("portfolio", today, f"{ticker}: {note}")
        )
        print(f"Narrative for {ticker}: {note}\n")
        write_narrative_note(ticker, note)
    price_df = pd.DataFrame(price_data)
    corr = rolling_correlation_matrix(price_df)
    for t1 in TICKERS:
        for t2 in TICKERS:
            conn.execute("""
                INSERT OR REPLACE INTO correlation_matrix (as_of_date, ticker_a, ticker_b, correlation)
                VALUES (?, ?, ?, ?)
            """, (today, t1, t2, float(corr.loc[t1, t2])))

    conn.commit()
    conn.close()
    print("\nPipeline run complete. Database updated.")

if __name__ == "__main__":
    run()