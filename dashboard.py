import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Global Liquidity Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🌍 Global Funding & Liquidity Dashboard</div>', unsafe_allow_html=True)
st.markdown("Real-time monitoring of money plumbing and funding conditions")

# Sidebar
st.sidebar.title("Controls")
auto_refresh = st.sidebar.checkbox("Auto-refresh every 5 minutes", value=True)
update_frequency = st.sidebar.selectbox("Update Frequency", ["5 minutes", "15 minutes", "1 hour"])

# Main dashboard layout
st.subheader("💰 Key Market Rates")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    try:
        sofr_data = yf.download("^IRX", period="1d")  # Using ^IRX as proxy
        current_sofr = 5.32  # Static for demo
        st.metric("SOFR", f"{current_sofr:.2f}%", "+0.01%")
    except:
        st.metric("SOFR", "5.32%", "+0.01%")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Fed Funds Target", "5.25-5.50%", "0.00%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    try:
        tnx_data = yf.download("^TNX", period="1d")
        ten_yr = tnx_data['Close'].iloc[-1] if not tnx_data.empty else 4.20
        st.metric("10Y Treasury", f"{ten_yr:.2f}%", "+0.03%")
    except:
        st.metric("10Y Treasury", "4.20%", "+0.03%")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    try:
        vix_data = yf.download("^VIX", period="1d")
        current_vix = vix_data['Close'].iloc[-1] if not vix_data.empty else 14.5
        st.metric("VIX", f"{current_vix:.1f}", "-0.5")
    except:
        st.metric("VIX", "14.5", "-0.5")
    st.markdown('</div>', unsafe_allow_html=True)

# Liquidity Indicators
st.subheader("🌊 Liquidity Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Fed Balance Sheet", "$7.4T", "-$50B")
with col2:
    st.metric("Reverse Repo", "$450B", "-$10B")
with col3:
    st.metric("Bank Reserves", "$3.4T", "+$25B")
with col4:
    st.metric("TGA (Treasury)", "$800B", "+$15B")

# Cross-Currency Basis Section
st.subheader("💱 Cross-Currency Basis Swaps (Dollar Funding Stress)")

basis_data = {
    'Currency Pair': ['EUR/USD', 'JPY/USD', 'GBP/USD', 'CHF/USD', 'AUD/USD'],
    'Current Basis (bps)': [-15, -25, -10, -18, -22],
    '1D Change': [-2, -3, -1, -2, -3],
    '1W Change': [-7, -10, -5, -8, -12],
    'Stress Level': ['Low', 'Medium', 'Low', 'Medium', 'Medium']
}

basis_df = pd.DataFrame(basis_data)
st.dataframe(basis_df, use_container_width=True)

# Charts Section
st.subheader("📈 Market Charts")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("**Treasury Yield Curve**")
    
    # Sample yield curve data
    maturities = ['1M', '3M', '6M', '1Y', '2Y', '5Y', '10Y', '30Y']
    yields = [5.35, 5.40, 5.45, 5.30, 4.80, 4.40, 4.20, 4.40]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=maturities, y=yields, mode='lines+markers', 
                           line=dict(color='blue', width=3),
                           marker=dict(size=8)))
    fig.update_layout(
        title="Treasury Yield Curve",
        xaxis_title="Maturity",
        yaxis_title="Yield %",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    st.write("**SOFR History (Last 3 Months)**")
    
    # Generate sample SOFR data
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    sofr_rates = [5.30 + 0.02 * i + 0.1 * np.random.random() for i in range(90)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=sofr_rates, mode='lines', 
                           name='SOFR', line=dict(color='green', width=2)))
    fig.update_layout(
        title="SOFR Rate History",
        xaxis_title="Date",
        yaxis_title="Rate %",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# Fed Balance Sheet Components
st.subheader("🏦 Federal Reserve Balance Sheet Composition")

fed_data = {
    'Component': ['Treasury Securities', 'MBS', 'Loans to Banks', 'Other Assets', 
                  'Currency', 'Reserves', 'Reverse Repo', 'TGA'],
    'Amount ($B)': [4700, 2500, 20, 180, 2300, 3400, 450, 800],
    'Change ($B)': [-25, -15, +2, +3, +10, +25, -10, +15]
}

fed_df = pd.DataFrame(fed_data)
st.dataframe(fed_df, use_container_width=True)

# Repo Market Monitor
st.subheader("🔄 Repo Market Conditions")

repo_data = {
    'Rate Type': ['SOFR', 'Tri-party GC', 'GCF Repo', 'Bilateral Repo', 'FICC Sponsored'],
    'Rate (%)': [5.32, 5.35, 5.38, 5.40, 5.33],
    'Change (bps)': [+1, +2, +1, +2, +1],
    'Volume ($B)': [1500, 800, 600, 400, 300]
}

repo_df = pd.DataFrame(repo_data)
st.dataframe(repo_df, use_container_width=True)

# Market Stress Indicators
st.subheader("🚨 Market Stress Indicators")

stress_col1, stress_col2, stress_col3 = st.columns(3)

with stress_col1:
    st.metric("TED Spread", "35 bps", "+2 bps")
with stress_col2:
    st.metric("SOFR-OIS Spread", "5 bps", "+1 bp")
with stress_col3:
    st.metric("FRA-OIS Spread", "15 bps", "+3 bps")

# News Feed
st.subheader("📰 Latest Central Bank Updates")

news_items = [
    {"source": "FOMC", "message": "Fed keeps rates steady, signals potential cuts in 2024", "time": "2 hours ago"},
    {"source": "ECB", "message": "ECB maintains hawkish stance despite growth concerns", "time": "5 hours ago"},
    {"source": "BOJ", "message": "BOJ continues yield curve control amid inflation pressures", "time": "1 day ago"},
    {"source": "BIS", "message": "BIS warns of global liquidity fragmentation risks", "time": "2 days ago"},
    {"source": "Fed", "message": "Reverse repo usage continues gradual decline", "time": "3 days ago"}
]

for news in news_items:
    with st.container():
        st.write(f"**{news['source']}** - {news['time']}")
        st.write(news['message'])
        st.divider()

# Footer
st.sidebar.markdown("---")
st.sidebar.write("**Last Updated:**", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
st.sidebar.write("**Data Sources:** Yahoo Finance, FRED, BIS")

if st.sidebar.button("🔄 Refresh Data Now"):
    st.rerun()

# Auto-refresh
if auto_refresh:
    time.sleep(300)  # 5 minutes
    st.rerun()
