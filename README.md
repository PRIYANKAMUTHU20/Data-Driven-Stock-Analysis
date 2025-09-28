# Data-Driven-Stock-Analysis
A complete workflow for extracting, file conversion, cleaning, analyzing, and visualizing stock market data.
- Extracts stock data from YAML files and converts it into CSV
- Maps stock data to sectors using a sector CSV file and clubbed it into a single CSV
- Cleans data (handles missing values, duplicates, fixes types, removes NAN values)
- Calculates key metrics: yearly returns, volatility, cumulative returns, sector performance, price correlation, monthly gainers/losers, and dumps into pkl files
- Visualizes results with plotly
- Interactive dashboard built with Streamlit
