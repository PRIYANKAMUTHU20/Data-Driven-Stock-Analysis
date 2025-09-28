import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle

# Page Config 
st.set_page_config(page_title="Interactive Stock Dashboard", layout="wide")

# Load Analysis
with open('all_analysis.pkl', 'rb') as f:
    data = pickle.load(f)  # 4 spaces inside the 'with' block

# Extract analysis
yearly_returns = data['yearly_returns']
top10_green = data['top10_green']
top10_loss = data['top10_loss']
market_summary = data['market_summary']
top10_volatility = data['top10_volatility']
top5_cum_stocks = data['top5_cum_stocks']
sector_perf = data['sector_perf']
corr_matrix = data['corr_matrix']
monthly_top = data['monthly_top']
df = data.get('df')  # main df for cumulative returns


# Fonts 

TITLE_FONT = dict(family="Georgia, serif", size=28, color="#1f2c56", weight="bold", style="italic")
AXIS_FONT = dict(family="Verdana, sans-serif", size=18, color="#2e3b55", weight="bold")
TICK_FONT = dict(family="Verdana, sans-serif", size=14, color="#2e3b55", weight="bold")
LEGEND_FONT = dict(family="Verdana, sans-serif", size=14, color="#2e3b55", weight="bold")
METRIC_FONT = dict(family="Georgia, serif", size=20, color="#1f2c56", weight="bold")


# Streamlit Title 
st.markdown(
    "<h1 style='text-align: center; font-size: 36px; font-family: Georgia, serif; color:#1f2c56; font-weight:bold; font-style:italic;'>Stock Market Dashboard</h1>",
    unsafe_allow_html=True
)


# Market Summary 
st.subheader("Market Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Green Stocks", market_summary["Green Stocks Count"])
col2.metric("Red Stocks", market_summary["Red Stocks Count"])
col3.metric("Average Price", round(market_summary["Average Price (all stocks)"], 2))
col4.metric("Average Volume", round(market_summary["Average Volume (all stocks)"], 2))

# Tabs 
tabs = st.tabs(["Top Gainers/Losers", "Volatility", "Cumulative Returns", "Sector Performance", "Correlation", "Monthly Performance"])

# Top Gainers / Losers 
def clean_bar_data(df, x_col, y_col):
    df = df.copy()
    df.columns = df.columns.str.strip()        # Strip column names
    df[x_col] = df[x_col].astype(str)         # Ensure x-axis is string
    df[y_col] = pd.to_numeric(df[y_col], errors='coerce')  # Ensure y-axis numeric
    df = df.dropna(subset=[x_col, y_col])     # Drop missing values
    return df
def style_chart(fig, title=""):
    fig.update_layout(
        title=title,
        title_font=dict(family="Georgia, serif", size=24, color="#1f2c56", weight="bold", style="italic"),
        xaxis=dict(title_font=dict(family="Verdana, sans-serif", size=18, color="#2e3b55", weight="bold"),
                   tickfont=dict(family="Verdana, sans-serif", size=14, color="#2e3b55", weight="bold")),
        yaxis=dict(title_font=dict(family="Verdana, sans-serif", size=18, color="#2e3b55", weight="bold"),
                   tickfont=dict(family="Verdana, sans-serif", size=14, color="#2e3b55", weight="bold")),
        legend=dict(font=dict(family="Verdana, sans-serif", size=14, color="#2e3b55", weight="bold")),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#f9f9f9"
    )
    return fig

with tabs[0]:
   
    top10_green_clean = clean_bar_data(top10_green, 'Ticker', 'yearly_return')
    fig = px.bar(top10_green_clean, x='Ticker', y='yearly_return', color_discrete_sequence=['green'])
    fig = style_chart(fig, title="Top 10 Green Stocks")
    st.plotly_chart(fig, use_container_width=True)

    
    top10_loss_clean = clean_bar_data(top10_loss, 'Ticker', 'yearly_return')
    fig = px.bar(top10_loss_clean, x='Ticker', y='yearly_return', color_discrete_sequence=['red'])
    fig = style_chart(fig, title="Top 10 Loss Stocks")
    st.plotly_chart(fig, use_container_width=True)

# Volatility 
with tabs[1]:
    
    top10_vol_clean = clean_bar_data(top10_volatility, 'Ticker', 'volatility')
    fig = px.bar(top10_vol_clean, x='Ticker', y='volatility', color_discrete_sequence=['orange'])
    fig = style_chart(fig, title="Top 10 Most Volatile Stocks")
    st.plotly_chart(fig, use_container_width=True)

# Cumulative Returns 
with tabs[2]:
    if df is not None:
        st.subheader("Cumulative Returns (Top 5 Highlighted)")
        fig = go.Figure()
        for ticker in df['Ticker'].unique():
            df_stock = df[df['Ticker']==ticker]
            fig.add_trace(go.Scatter(x=df_stock['date'], y=df_stock['cumulative_return'],
                                     mode='lines', line=dict(color='lightgrey', width=1),
                                     name=ticker, showlegend=False, opacity=0.7))
        colors = ['blue','green','red','orange','purple']
        for i, ticker in enumerate(top5_cum_stocks):
            df_stock = df[df['Ticker']==ticker]
            fig.add_trace(go.Scatter(x=df_stock['date'], y=df_stock['cumulative_return'],
                                     mode='lines', line=dict(color=colors[i], width=3),
                                     name=ticker))
        fig.update_layout(title="Cumulative Return Over Time",
                          title_font=TITLE_FONT,
                          xaxis_title="Date",
                          yaxis_title="Cumulative Return",
                          xaxis=dict(title_font=AXIS_FONT, tickfont=TICK_FONT),
                          yaxis=dict(title_font=AXIS_FONT, tickfont=TICK_FONT),
                          legend=dict(font=LEGEND_FONT))
        st.plotly_chart(fig, use_container_width=True)

# Sector Performance
with tabs[3]:
  
    sector_perf_clean = clean_bar_data(sector_perf, 'sector', 'yearly_return')
    fig = px.bar(sector_perf_clean, x='sector', y='yearly_return', color_discrete_sequence=['skyblue'])
    fig = style_chart(fig, title="Average Yearly Return by Sector")
    st.plotly_chart(fig, use_container_width=True)
# Correlation 
with tabs[4]:
    if df is not None:
       
        top_stocks = df.groupby('Ticker')['close'].mean().sort_values(ascending=False).head(20).index
        subset_corr = corr_matrix.loc[top_stocks, top_stocks]

        fig = px.imshow(
            subset_corr,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            aspect="auto",  # maintains square-ish cells
            width=1000,     # wider figure
            height=800      # taller figure
        )

        fig.update_layout(
            title="Top 20 Stocks Price Correlation",
            title_font=dict(family="Arial", size=24, color="black", weight="bold"),
            xaxis=dict(tickangle=45, tickfont=dict(family="Arial", size=14, color="black")),
            yaxis=dict(tickfont=dict(family="Arial", size=14, color="black"))
        )
        st.plotly_chart(fig, use_container_width=True)

#  Monthly Performance 
   
with tabs[5]:
    st.subheader("Monthly Top 5 Gainers / Losers")
    months = list(monthly_top.keys())
    selected_month = st.selectbox("Select Month", months)
    top_gainers = monthly_top[selected_month]['Top Gainers']
    top_losers = monthly_top[selected_month]['Top Losers']

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(top_gainers, x='Ticker', y='monthly_return',
                     color_discrete_sequence=['green'], labels={'monthly_return':'Monthly Return (%)'},
                     title=f'Top 5 Gainers - {selected_month}')
        fig.update_layout(title_font=TITLE_FONT,
                          xaxis=dict(title_font=AXIS_FONT, tickfont=TICK_FONT),
                          yaxis=dict(title_font=AXIS_FONT, tickfont=TICK_FONT))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(top_losers, x='Ticker', y='monthly_return',
                     color_discrete_sequence=['red'], labels={'monthly_return':'Monthly Return (%)'},
                     title=f'Top 5 Losers - {selected_month}')
        fig.update_layout(title_font=TITLE_FONT,
                          xaxis=dict(title_font=AXIS_FONT, tickfont=TICK_FONT),
                          yaxis=dict(title_font=AXIS_FONT, tickfont=TICK_FONT))
        st.plotly_chart(fig, use_container_width=True)

