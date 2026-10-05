from fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("finance-tools")

@mcp.tool()
def get_price_history(ticker: str, period: str = "6mo") -> dict:
    """Fetch historical daily closing prices for a stock ticker."""
    data = yf.Ticker(ticker).history(period=period)
    return {
        "ticker": ticker,
        "dates": data.index.strftime("%Y-%m-%d").tolist(),
        "close": data["Close"].round(2).tolist(),
    }

@mcp.tool()
def get_fundamentals(ticker: str) -> dict:
    """Fetch basic fundamentals: P/E ratio, market cap, sector, beta."""
    info = yf.Ticker(ticker).info
    return {
        "ticker": ticker,
        "trailing_pe": info.get("trailingPE"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
        "beta": info.get("beta"),
    }

if __name__ == "__main__":
    mcp.run()