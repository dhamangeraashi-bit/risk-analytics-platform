import streamlit as st
import plotly.graph_objects as go

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .metric-card {
        background: #161B22; border: 1px solid #2D333B;
        border-radius: 12px; padding: 20px; margin-bottom: 10px;
    }
    .metric-label { color: #8B949E; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-value { color: #E6EDF3; font-size: 28px; font-weight: 600; }
    .metric-delta-positive { color: #2DD4BF; font-size: 14px; }
    .metric-delta-negative { color: #F87171; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

def metric_card(label, value, delta=None, positive=True, live=False):
    delta_html = ""
    if delta:
        cls = "metric-delta-positive" if positive else "metric-delta-negative"
        arrow = "▲" if positive else "▼"
        delta_html = f'<div class="{cls}">{arrow} {delta}</div>'
    live_html = '<span style="color:#2DD4BF; font-size:11px; font-weight:600;">● LIVE</span>' if live else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label} {live_html}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def styled_line_chart(dates, values, title, y_suffix="%"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values, mode="lines",
        line=dict(color="#2DD4BF", width=2.5),
        fill="tozeroy", fillcolor="rgba(45, 212, 191, 0.1)"
    ))
    fig.update_layout(
        title=title,
        plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
        font=dict(color="#E6EDF3"),
        xaxis=dict(gridcolor="#2D333B", showgrid=True),
        yaxis=dict(gridcolor="#2D333B", showgrid=True, ticksuffix=y_suffix),
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,
    )
    return fig

def styled_heatmap(corr_df, title="Correlation Matrix"):
    fig = go.Figure(data=go.Heatmap(
        z=corr_df.values, x=corr_df.columns, y=corr_df.index,
        colorscale=[[0, "#F87171"], [0.5, "#161B22"], [1, "#2DD4BF"]],
        zmin=-1, zmax=1, text=corr_df.round(2).values, texttemplate="%{text}",
    ))
    fig.update_layout(
        title=title, plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
        font=dict(color="#E6EDF3"), margin=dict(l=20, r=20, t=40, b=20), height=350,
    )
    return fig

GLOSSARY = {
    "Sharpe Ratio": "Measures return earned per unit of risk taken, versus a safe risk-free investment. Higher is better — above 1 is considered good, above 2 is strong.",
    "Sortino Ratio": "Like Sharpe, but only penalizes downside risk (losses), not all volatility. A more investor-realistic version of Sharpe.",
    "Max Drawdown": "The worst peak-to-trough loss an investor would have experienced holding this asset. Always negative or zero.",
    "Annualized Volatility": "How much the price swings around its average, scaled to a yearly figure. Higher means bigger price swings.",
    "95% VaR": "On a bad day (the worst 5% of days), roughly how much you could expect to lose.",
    "Correlation": "How much two assets move together. Near 0 means independent movement — useful for diversification.",
}

def glossary_expander():
    with st.expander("📖 What do these terms mean?"):
        for term, definition in GLOSSARY.items():
            st.markdown(f"**{term}** — {definition}")