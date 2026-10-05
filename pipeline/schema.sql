CREATE TABLE IF NOT EXISTS securities (
    ticker TEXT PRIMARY KEY,
    name TEXT,
    sector TEXT
);

CREATE TABLE IF NOT EXISTS prices (
    ticker TEXT REFERENCES securities(ticker),
    date TEXT,
    close REAL,
    PRIMARY KEY (ticker, date)
);

CREATE TABLE IF NOT EXISTS risk_metrics (
    ticker TEXT REFERENCES securities(ticker),
    as_of_date TEXT,
    annualized_return REAL,
    annualized_volatility REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    max_drawdown REAL,
    var_95 REAL,
    PRIMARY KEY (ticker, as_of_date)
);

CREATE TABLE IF NOT EXISTS correlation_matrix (
    as_of_date TEXT,
    ticker_a TEXT,
    ticker_b TEXT,
    correlation REAL,
    PRIMARY KEY (as_of_date, ticker_a, ticker_b)
);

CREATE TABLE IF NOT EXISTS narratives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope TEXT,
    as_of_date TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS inclusion_metrics (
    region TEXT,
    year INTEGER,
    fi_index REAL,
    upi_transactions_per_capita REAL,
    bank_account_penetration REAL,
    PRIMARY KEY (region, year)
);