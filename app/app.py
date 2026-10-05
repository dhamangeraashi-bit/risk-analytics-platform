import streamlit as st
import sqlite3
import pandas as pd
import os
from charts import inject_css, metric_card, styled_line_chart, styled_heatmap, glossary_expander
from ask_ai import ask_about_data

st.set_page_config(page_title="Risk Analytics Platform", layout="wide", page_icon="📊")
inject_css()

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "analytics.db")
conn = sqlite3.connect(DB_PATH, check_same_thread=False)

st.title("📊 AI-Augmented Risk Analytics Platform")
st.caption("Live portfolio risk metrics, grounded AI commentary, and a financial inclusion module — built on free-tier infrastructure end to end.")

tab1, tab2 = st.tabs(["Portfolio Risk Analytics", "Financial Inclusion"])

with tab1:
    tickers = pd.read_sql("SELECT DISTINCT ticker FROM risk_metrics", conn)["ticker"].tolist()
    selected = st.multiselect("Select tickers", tickers, default=tickers, key="portfolio_tickers")
    glossary_expander()

    if selected:
        placeholders = ",".join("?" * len(selected))
        metrics_df = pd.read_sql(
            f"SELECT * FROM risk_metrics WHERE ticker IN ({placeholders}) "
            f"AND as_of_date = (SELECT MAX(as_of_date) FROM risk_metrics)",
            conn, params=selected
        )

        cols = st.columns(len(selected))
        for i, ticker in enumerate(selected):
            row = metrics_df[metrics_df["ticker"] == ticker].iloc[0]
            hist = pd.read_sql(
                "SELECT * FROM risk_metrics WHERE ticker = ? ORDER BY as_of_date DESC LIMIT 2",
                conn, params=(ticker,)
            )
            sharpe_delta, sharpe_positive = None, True
            if len(hist) == 2:
                diff = hist.iloc[0]["sharpe_ratio"] - hist.iloc[1]["sharpe_ratio"]
                sharpe_positive = diff >= 0
                sharpe_delta = f"{diff:+.2f} vs prior run"
            with cols[i]:
                st.subheader(ticker)
                metric_card("Sharpe Ratio", f"{row['sharpe_ratio']:.2f}", sharpe_delta, sharpe_positive, live=True)
                metric_card("Annualized Return", f"{row['annualized_return']*100:.1f}%")
                metric_card("Max Drawdown", f"{row['max_drawdown']*100:.1f}%", positive=False)

        st.subheader("Price Trend (6-month)")
        price_cols = st.columns(len(selected))
        for i, ticker in enumerate(selected):
            prices = pd.read_sql(
                "SELECT date, close FROM prices WHERE ticker = ? ORDER BY date",
                conn, params=(ticker,)
            )
            with price_cols[i]:
                st.plotly_chart(
                    styled_line_chart(prices["date"], prices["close"], f"{ticker} Closing Price", y_suffix=""),
                    use_container_width=True, key=f"price_{ticker}"
                )

        st.subheader("Correlation Matrix")
        corr_df = pd.read_sql(
            f"""SELECT * FROM correlation_matrix
                WHERE ticker_a IN ({placeholders})
                AND as_of_date = (SELECT MAX(as_of_date) FROM correlation_matrix)""",
            conn, params=selected
        )
        if not corr_df.empty:
            pivot = corr_df.pivot(index="ticker_a", columns="ticker_b", values="correlation")
            st.plotly_chart(styled_heatmap(pivot), use_container_width=True)

        st.subheader("AI Narrative")
        narratives = pd.read_sql(
            "SELECT summary FROM narratives WHERE scope='portfolio' ORDER BY id DESC LIMIT 5",
            conn
        )
        for _, row in narratives.iterrows():
            st.info(row["summary"])

        st.subheader("Learn More")
        st.markdown("""
        - [Investopedia: Sharpe Ratio Explained](https://www.investopedia.com/terms/s/sharperatio.asp)
        - [Investopedia: Understanding Maximum Drawdown](https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp)
        - [Investopedia: Value at Risk (VaR)](https://www.investopedia.com/terms/v/var.asp)
        """)

        st.subheader("💬 Ask AI About This Data")
        question = st.text_input("Ask a question about the numbers above")
        if question:
            with st.spinner("Thinking..."):
                answer = ask_about_data(question, metrics_df.to_dict())
            st.write(answer)
    else:
        st.warning("Select at least one ticker above.")

with tab2:
    st.header("Financial Inclusion Gap Analysis")
    st.caption("Sources: RBI Financial Inclusion Index publications; NPCI UPI statistics. "
               "Figures are compiled manually from public releases; see README for citations.")

    inclusion_df = pd.read_sql("SELECT * FROM inclusion_metrics", conn)

    if inclusion_df.empty:
        st.info(
            "This module isn't populated with data yet — it reads from the "
            "`inclusion_metrics` table, filled once RBI Financial Inclusion Index "
            "values and NPCI UPI statistics are sourced and loaded."
        )
    else:
        region = st.selectbox("Region", inclusion_df["region"].unique())
        region_data = inclusion_df[inclusion_df["region"] == region].sort_values("year")
        st.plotly_chart(
            styled_line_chart(region_data["year"].astype(str), region_data["fi_index"],
                               f"{region} — Financial Inclusion Index", y_suffix=""),
            use_container_width=True
        )