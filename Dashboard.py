import streamlit as st
import yfinance as yf
from datetime import date, timedelta
import pandas as pd


# Define S&P 500 symbol
sp500_symbol = "^GSPC"


# Define top 50 companies by market cap (replace with your preferred source)
top_companies = {
    "Apple": "AAPL",
    "Saudi Aramco": "2222.SR",
    # ... add remaining companies and their symbols
}


# Get user selection
selected_symbols = st.multiselect("Select Stocks:", list(top_companies.keys()))
symbols = [top_companies[symbol] for symbol in selected_symbols]


# Get start and end date
default_end_date = date.today()
default_start_date = default_end_date - timedelta(days=30)
start_date = st.date_input("Start Date:", default_start_date)
end_date = st.date_input("End Date:", default_end_date)


# User-defined window for rolling correlation and volatility
correlation_window = st.slider("Rolling Correlation Window:", 10, 200, 50)
volatility_window = st.slider("Rolling Volatility Window:", 10, 200, 50)


# Fetch data only if symbols are selected and dates are valid
if symbols and start_date <= end_date:
    company_data = yf.download([*symbols, sp500_symbol], start=start_date, end=end_date)


# Display stock information and charts
if company_data.empty:
    st.write("No data found for selected symbols or dates.")
else:
    # Calculate daily returns for all stocks (including S&P 500)
    for symbol, data in company_data.iterrows():
        data["Daily Return"] = data["Close"].pct_change()

    # Calculate rolling correlation and volatility for selected stocks
    for symbol in selected_symbols:
        rolling_correlation = company_data[symbol]["Daily Return"].rolling(
            window=correlation_window
        ).corr(company_data[sp500_symbol]["Daily Return"])
        company_data[f"{symbol}-S&P 500 Correlation"] = rolling_correlation

        data["Volatility"] = data["Daily Return"].rolling(window=volatility_window).std() * np.sqrt(252)

    # Prepare summary table data
    summary_data = {
        "Symbol": [*selected_symbols, sp500_symbol],
        "Price": company_data["Close"].iloc[-1, :],
        "Daily Return": company_data["Daily Return"].iloc[-1, :],
        "Volatility": company_data["Volatility"].iloc[-1, :],
    }
    if selected_symbols:
        summary_data[f"{selected_symbols[0]}-S&P 500 Correlation"] = company_data[
            f"{selected_symbols[0]}-S&P 500 Correlation"
        ].iloc[-1, :]
        for symbol in selected_symbols[1:]:
            summary_data[f"{symbol}-S&P 500 Correlation"] = company_data[
                f"{symbol}-S&P 500 Correlation"
            ].iloc[-1, :]

    summary_df = pd.DataFrame(summary_data)

    # Display information and charts for each selected stock
    for symbol, data in company_data.iterrows():
        if symbol in selected_symbols:
            st.header(f"{symbol} - {data['shortName'].iloc[0]}")

            # Existing code for price chart, daily return, moving average (optional), and volatility (optional)

            # Chart for rolling correlation with S&P 500
            st.subheader(f"Rolling Correlation with S&P 500")
            st.line_chart(data[f"{symbol}-S&P 500 Correlation"])

            st.markdown("---")

    # Display summary table
    st.subheader("Summary Table")
    st.dataframe(summary_df.style.set_precision(2))


# Run the app
if __name__ == "__main__":
    st.title(
        "Stock Price Tracker with Moving Averages, Daily Returns, Rolling Volatility, and Correlation with S
