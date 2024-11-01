import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
from io import BytesIO

# Function to download data as CSV
def download_stock_report(stock_df, ticker):
    buffer = BytesIO()
    stock_df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

# Streamlit app title and description
st.set_page_config(page_title="Indian Stock Market Analysis", page_icon="📈")
st.title("📈 Indian Stock Market Analysis App")
st.write("Analyze Indian stocks and download stock reports as CSV files.")

# Input for ticker symbol
st.sidebar.header("Stock Ticker Input")
ticker = st.sidebar.text_input("Enter Indian stock ticker symbol (e.g., RELIANCE.NS, TCS.NS):")

# Date range for data
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End date", value=pd.to_datetime("today"))

# Select metric to plot
metric = st.sidebar.selectbox("Select metric to display", ['Open', 'High', 'Low', 'Close', 'Volume'])

# Fetch data and show only if ticker is entered
if ticker:
    # Fetching stock data from Yahoo Finance
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if not stock_data.empty:
        st.subheader(f"Stock Data for {ticker}")

        # Displaying the data table in a cleaner format
        st.write("Stock Data Table", stock_data)

        # Ensure 'Date' column is properly formatted
        stock_data.reset_index(inplace=True)
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Ensure 'Date' is in datetime format

        # Displaying selected metric with Altair for better customization
        if metric in stock_data.columns:
            st.write(f"### {metric} Price Over Time")

            # Altair chart
            chart = alt.Chart(stock_data).mark_line(color='green').encode(
                x=alt.X('Date:T', title='Date'),
                y=alt.Y(f'{metric}:Q', title=metric),
                tooltip=[alt.Tooltip('Date:T'), alt.Tooltip(f'{metric}:Q')]
            ).interactive()

            st.altair_chart(chart, use_container_width=True)
        else:
            st.error(f"Selected metric '{metric}' is not available in the data.")
        
        # Download button for CSV
        csv_buffer = download_stock_report(stock_data, ticker)
        st.download_button(
            label="📥 Download Stock Report",
            data=csv_buffer,
            file_name=f"{ticker}_stock_report.csv",
            mime="text/csv"
        )
    else:
        st.error("No data found for the given ticker symbol. Please ensure you're using the correct symbol (e.g., RELIANCE.NS for NSE).")
else:
    st.info("Please enter a stock ticker symbol to get started.")

# Footer with app information
st.sidebar.markdown("""
---
**About this app**

Created using [Streamlit](https://streamlit.io) and [yfinance](https://pypi.org/project/yfinance/).
""")
